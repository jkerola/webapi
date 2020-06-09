import json
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_assets import Bundle, Environment
from json2html import *


app7 = Flask(__name__)



@app7.route("/")
def index():
    return "Hello, please go to http://127.0.0.1:7000/home/ for the home page"




@app7.route("/home/")
def home():
    return render_template('home.html')


# users
@app7.route("/users/", methods=['GET'])
def users():
    return render_template('users.html')

# batches
@app7.route("/batches/", methods=['GET'])
def batches():
    return render_template('batches.html')

# reviews
@app7.route("/reviews/", methods=['GET'])
def reviews():
    return render_template('reviews.html')












if __name__ == '__main__':
    app7.run(port=7000, debug=True)

