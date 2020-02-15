from gcoffee import db
from datetime import datetime


class User(db.Model):
    '''Default user model'''
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    # relationships
    batches = db.relationship('Batch', backref='batch_brewer', cascade='all, delete-orphan', lazy=True)
    reviews = db.relationship('Review', backref='review_author', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'User[ {self.student_id} ]'


class Review(db.Model):
    '''Review model'''
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    # relationships
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'Review[ Batch #{self.batch_id:} ({self.value} / 10) ]'


class Batch(db.Model):
    '''Coffee batch model'''
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default='10')
    date_brewed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # relationships
    location = db.Column(db.Integer, db.ForeignKey('location.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    coffee = db.Column(db.Integer, db.ForeignKey('coffee.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    brewer = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    reviews = db.relationship('Review', backref='batch_review', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'Batch[ {self.id}: by {self.brewer} on {self.date_brewed} ]'


class Coffee(db.Model):
    '''Coffee model'''
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, default='Unknown Brand')
    # relationships
    batches = db.relationship('Batch', backref='batch_coffee', lazy=True)

    def __repr__(self):
        return f'Coffee[ {self.name} ]'


class Location(db.Model):
    '''Coffee batch location model'''
    # attributes
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, default='Unknown Location')
    # relationships
    batches = db.relationship('Batch', backref='batch_location', lazy=True)

    def __repr__(self):
        return f'Location[ {self.name} ]'
