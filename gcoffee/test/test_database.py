import os
import pytest
import tempfile
from gcoffee.models import User, Review, Location, Batch, Coffee
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, InterfaceError
from sqlalchemy import event
from gcoffee import db
import app

# setup from lovelace instructions
# https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/testing-flask-applications/#unit-testing
@pytest.fixture
def db_handle():
    '''Create a temporary database for testing'''
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    context = app.app.app_context()
    context.push()

    with app.app.app_context():
        db.create_all()

    yield db

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class TestDatabaseModels(object):
    '''create objects for testing'''
    # setup methods
    def get_user(self, id='1234567'):
        return User(student_id=id)

    def get_coffee(self, name='Pirkka Dark Roast'):
        return Coffee(name=name)

    def get_location(self, location='Guild Room'):
        return Location(name=location)

    def get_review(self, user, batch, value=10):
        review = Review(
            author_id=user.id,
            batch_id=batch.id,
            value=value
        )
        return review

    def get_batch(self, user, location, coffee):
        batch = Batch(
            brewer=user.id,
            location=location.id,
            coffee=coffee.id
        )
        return batch

    # test methods
    def test_database_exists(self, db_handle):
        '''Test wether database creation is succesfull'''
        assert db_handle

    def test_create_instances(self, db_handle):
        '''Create and test model instances in database'''
        user = self.get_user()
        location = self.get_location()
        coffee = self.get_coffee()
        db_handle.session.add(user)
        db_handle.session.add(coffee)
        db_handle.session.add(location)
        db_handle.session.commit()
        assert User.query.filter_by(student_id=1234567).scalar()
        assert Coffee.query.filter_by(name='Pirkka Dark Roast').scalar()
        assert Location.query.filter_by(name='Guild Room').scalar()

        # Create a batch from model
        batch = self.get_batch(user, location, coffee)
        db_handle.session.add(batch)
        db_handle.session.commit()
        assert Batch.query.filter_by(brewer=user.id).scalar()

        # create a review for batch
        review = self.get_review(user, batch)
        db_handle.session.add(review)
        db_handle.session.commit()
        assert Review.query.filter_by(author_id=user.id).scalar()

    def test_duplicate_names(self, db_handle):
        '''Test for Integrity error with duplicate unique values'''
        self.test_create_instances(db_handle)
        dup_user = self.get_user()
        dup_coffee = self.get_coffee()
        dup_location = self.get_location()

        db_handle.session.add(dup_user)
        db_handle.session.add(dup_coffee)
        db_handle.session.add(dup_location)
        with pytest.raises(IntegrityError):
            db_handle.session.commit()
        db_handle.session.rollback

    def test_relationships(self, db_handle):
        '''Test for table relationship functionality'''
        self.test_create_instances(db_handle)
        review = Review.query.first()
        user = User.query.first()
        batch = Batch.query.first()
        coffee = Coffee.query.first()
        location = Location.query.first()

        assert batch.brewer == user.id
        assert batch.coffee == coffee.id
        assert batch.location == location.id
        assert batch.reviews[0] == review
        assert review.author_id == user.id

    def test_missing_parameters(self, db_handle):
        '''Test for Error handling with missing parameters and objects'''
        invalid_batch = Batch()
        invalid_user = User()
        db_handle.session.add(invalid_batch)
        db_handle.session.add(invalid_user)
        with pytest.raises(IntegrityError):
            db.session.commit()
            db.session.rollback()

    def test_invalid_parameters(self, db_handle):
        '''Test for error handling with invalid parameter values'''
        invalid_user = self.get_user('Student Name')
        db_handle.session.add(invalid_user)
        print('\ntest_invalid_parameters() --Bypassed, see comment')
        # with pytest.raises(InterfaceError):
        db_handle.session.commit()         # ** see below
        db_handle.session.rollback()

        # ** This should raise an InterfaceError due to conflicting datatypes,
        # however SQLite accepts any value into any field without complaint.
        # I'm leaving this in incase we swap to PostgreSQL later on.

    def test_delete_object(self, db_handle):
        '''Test if cascading relationships function on delete'''
        self.test_create_instances(db_handle)
        user = User.query.first()
        db_handle.session.delete(user)
        db_handle.session.commit()
        assert User.query.count() == 0
        assert Batch.query.count() == 0
        assert Review.query.count() == 0

        # Test if location, coffee still exist in db
        assert Coffee.query.count() == 1
        assert Location.query.count() == 1

    def test_delete_object_batch(self, db_handle):
        '''Test if cascading relationships function on delete, one further'''
        self.test_create_instances(db_handle)
        batch = Batch.query.first()
        db_handle.session.delete(batch)
        db_handle.session.commit()
        # Check that batches and reviews were deleted
        assert Batch.query.count() == 0
        assert Review.query.count() == 0
        # Check if users, coffees and locations still exist
        assert User.query.count() == 1
        assert Coffee.query.count() == 1
        assert Location.query.count() == 1

    def test_update_object(self, db_handle):
        '''Test if cascading relationships function on parameter update'''
        self.test_create_instances(db_handle)
        User.query.first().id = 9  # primary key
        db_handle.session.commit()
        batch = Batch.query.first()
        review = Review.query.first()
        assert batch.brewer == 9
        assert review.author_id == 9

    def test_update_missing_object(self, db_handle):
        '''Test if updating non-existing tables raises error'''
        with pytest.raises(AttributeError):
            user = User.query.first()
            user.student_id = 1222020
            db_handle.session.commit()

        # Test updating recently deleted object
        self.test_create_instances(db_handle)
        batch = Batch.query.first()
        db_handle.session.delete(batch)
        db_handle.session.commit()

        with pytest.raises(AttributeError):
            Batch.query.first().amount = 2