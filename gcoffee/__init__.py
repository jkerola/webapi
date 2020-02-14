from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gcoffee.config import Config

app = Flask(__name__)
db = SQLAlchemy()


def create_app(config=Config):
    '''Create flask app'''
    app.config.from_object(config)
    db.init_app(app)
    return app
