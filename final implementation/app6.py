import json
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app6 = Flask(__name__)
app6.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app6.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app6.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app6)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(64), unique=True, nullable=False)
    has_batches = db.relationship('Batch', back_populates='user')
    has_reviews = db.relationship('Review', back_populates='user')

    # def __repr__(self):
    #     return f"Prodct('{self.id}', '{self.handle}', '{self.weight}', '{self.price}', '{self.in_storage}')"


class Batch(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date_brewed = db.Column(db.Integer, nullable=True)
    coffee = db.Column(db.Integer, nullable=False)
    location = db.Column(db.Integer, nullable=False)

    brewer = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship('User', back_populates='has_batches')
    # def __repr__(self):
    #     return f"StorageItem('{self.id}', '{self.qty}', '{self.product_id}', '{self.location}')"

class Review(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey("batch.id"), nullable=False)

    user = db.relationship('User', back_populates='has_reviews')

    # def __repr__(self):
    #     return f"StorageItem('{self.id}', '{self.qty}', '{self.product_id}', '{self.location}')"


db.create_all()

@app6.route("/")
def index():
    return "Hello"



#get users collection
@app6.route("/api/users/", methods=['GET'])
def get_users():
    my_list = []
    inventoryList = []
    users = User.query.all()
    for user in users:
        recordObject = {'student_id': user.student_id}
        my_list.append(recordObject)

    return json.dumps(my_list)

#get a user
@app6.route("/api/users/<student_id>", methods=['GET'])
def get_user(student_id):
    try:
        wanted_user = User.query.filter_by(student_id=student_id).first()
        if wanted_user: 
            recordObject = {'user_id': wanted_user.id,
            'student_id': wanted_user.student_id}
            return recordObject, 200
        else:
            return "Student id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#delete a user
@app6.route("/api/users/<student_id>/", methods=['DELETE'])
def delete_user(student_id):
    try:
        wanted_user = User.query.filter_by(student_id=student_id).first()
        if wanted_user:
            db.session.delete(wanted_user)
            db.session.commit()
            return "User was deleted", 200
        else:
            return "Student id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#edit a user
@app6.route("/api/users/<student_id>", methods=['PUT'])
def edit_user(student_id):
    try:
        wanted_user = User.query.filter_by(student_id=student_id).first()
        if wanted_user: 
            updated_student_id = int(request.json["student_id"])
            wanted_user.student_id=updated_student_id
            db.session.commit()
            return "User was successfully updated", 201
        else:
            return "Student id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#add user
@app6.route("/api/users/", methods=['POST'])
def add_user():
    if "{" in request.data.__str__() and "}" in request.data.__str__():
        try:
            student_id = int(request.json["student_id"])
            new_user_exist = User.query.filter_by(student_id=student_id).first()
            if new_user_exist:
                return "User already exists", 409            
            try:
                student_id = int(request.json["student_id"])
                new_user = User(
                    student_id=student_id)
                db.session.add(new_user)
                db.session.commit()
                return "User was added", 201
            except (KeyError, ValueError, IntegrityError):
                return "Data entered is incorrect", 400
        except (KeyError, ValueError, IntegrityError):
            return "Incomplete request - missing fields", 400
    return "Request content type must be JSON", 415






#get batches collection
@app6.route("/api/batches/", methods=['GET'])
def get_batches():
    my_list = []
    batchList = []
    batches = Batch.query.all()
    for batch in batches:
        recordObject = {'amount': batch.amount,
        'date_brewed': batch.date_brewed,
        'brewer': batch.brewer,
        'coffee': batch.coffee,
        'location': batch.location,
        }
        my_list.append(recordObject)

    return json.dumps(my_list)

#get a batch
@app6.route("/api/batches/<batch_id>/", methods=['GET'])
def get_batch(batch_id):
    try:
        wanted_batch = Batch.query.filter_by(id=batch_id).first()
        wanted_user = User.query.filter_by(id=wanted_batch.brewer).first()
        if wanted_batch: 
            recordObject = {'batch_id': wanted_batch.id,
            'amount': wanted_batch.amount,
            "date_brewed": wanted_batch.date_brewed,
            'brewer_studnet_id': wanted_user.student_id,
            'coffee': wanted_batch.coffee,
            'location': wanted_batch.location
            }
            return recordObject, 200
        else:
            return "Batch id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415


#delete a batch
@app6.route("/api/batches/<batch_id>/", methods=['DELETE'])
def delete_batch(batch_id):
    try:
        wanted_batch = Batch.query.filter_by(id=batch_id).first()
        if wanted_batch:
            db.session.delete(wanted_batch)
            db.session.commit()
            return "Batch was deleted", 200
        else:
            return "Batch id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415


#edit a batch
@app6.route("/api/batches/<batch_id>/", methods=['PUT'])
def edit_batch(batch_id):
    try:
        wanted_batch = Batch.query.filter_by(id=batch_id).first()
        if wanted_batch:
            updated_amount = int(request.json["amount"])
            wanted_batch.amount=updated_amount
            updated_date_brewed = int(request.json["date_brewed"])
            wanted_batch.date_brewed=updated_date_brewed
            updated_brewer = int(request.json["brewer"])
            wanted_batch.brewer=updated_brewer
            updated_coffee = int(request.json["coffee"])
            wanted_batch.coffee=updated_coffee
            updated_location = int(request.json["location"])
            wanted_batch.location=updated_location
            db.session.commit()
            return "Batch was successfully updated", 201
        else:
            return "Batch id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#add batch
@app6.route("/api/users/<student_id>/batches/", methods=['POST'])
def add_to_batches(student_id):
    try:
        wanted_user = User.query.filter_by(student_id=student_id).first()
        if wanted_user:
            try:
                location = int(request.json["location"])
                coffee = int(request.json["coffee"])
                amount = int(request.json["amount"])
                date_brewed = int(request.json["date_brewed"])
                brewer = wanted_user.id
                to_be_added_batch = Batch(
                    amount=amount, brewer=brewer, location=location, coffee=coffee, date_brewed=date_brewed)
                db.session.add(to_be_added_batch)
                db.session.commit()
                return "batch was added successfully", 201
            except(KeyError, ValueError, IntegrityError):
                return "Data entered is not in the right format", 400

        else:
            return "User not found", 404

    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415




#get reviews collection
@app6.route("/api/reviews/", methods=['GET'])
def get_reviews():
    my_list = []
    reviewList = []
    reviews = Review.query.all()
    for review in reviews:
        recordObject = {'value': review.value,
        'author_id': review.author_id,
        'batch_id': review.batch_id
        }
        my_list.append(recordObject)

    return json.dumps(my_list)

#get a review
@app6.route("/api/reviews/<review_id>/", methods=['GET'])
def get_review(review_id):
    try:
        wanted_review = Review.query.filter_by(id=review_id).first()
        wanted_user = User.query.filter_by(id=wanted_review.author_id).first()
        if wanted_review: 
            recordObject = {'review_id': wanted_review.id,
            'value': wanted_review.value,
            'author_student_id': wanted_user.student_id,
            'batch_id': wanted_review.batch_id
            }
            return recordObject, 200
        else:
            return "Review id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#delete a review
@app6.route("/api/reviews/<review_id>/", methods=['DELETE'])
def delete_review(review_id):
    try:
        wanted_review = Review.query.filter_by(id=review_id).first()
        if wanted_review:
            db.session.delete(wanted_review)
            db.session.commit()
            return "Review was deleted", 200
        else:
            return "Review id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415


#edit a review
@app6.route("/api/reviews/<review_id>/", methods=['PUT'])
def edit_review(review_id):
    try:
        wanted_review = Review.query.filter_by(id=review_id).first()
        updated_student_id = int(request.json["student_id"])
        wanted_user = User.query.filter_by(student_id=updated_student_id).first()
        updated_batch_id = int(request.json["batch_id"])
        wanted_batch = Batch.query.filter_by(id=updated_batch_id).first()

        if wanted_review and wanted_user and wanted_batch:
            updated_value = int(request.json["value"])
            wanted_review.value=updated_value

            wanted_review.author_id = wanted_user.id
            wanted_review.batch_id=updated_batch_id

            db.session.commit()
            return "Review was successfully updated", 201
        else:
            return "Review id or student id or batch id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

#add review
@app6.route("/api/batches/<batch_id>/reviews/", methods=['POST'])
def add_to_reviews(batch_id):
    try:
        wanted_batch = Batch.query.filter_by(id=batch_id).first()
        student_id = int(request.json["student_id"])
        wanted_user = User.query.filter_by(student_id=student_id).first()
        if wanted_batch and wanted_user:
            try:
                value = int(request.json["value"])
                author_id = wanted_user.id
                batch_id = wanted_batch.id
                to_be_added_review = Review(
                    value=value, batch_id=batch_id, author_id=author_id)
                db.session.add(to_be_added_review)
                db.session.commit()
                return "review was added successfully", 201
            except(KeyError, ValueError, IntegrityError):
                return "Data entered is not in the right format", 400
        else:
            return "Batch or student id not found", 404
    except (KeyError, ValueError, IntegrityError):
        return "Request content type must be JSON", 415

        

if __name__ == '__main__':
    app6.run(port=5000, debug=True)
