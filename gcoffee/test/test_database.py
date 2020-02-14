import os
import pytest
import tempfile
from gcoffee.models import User, Review, Location, Batch, Coffee
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy import event
from gcoffee import db
import app

# setup from lovelace instructions
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
