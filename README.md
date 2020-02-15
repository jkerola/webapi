# Guild Coffee; a brewer tracking api
=====================================
## Setup
We recommend you install and create a virtual enviroment first, then install the required extensions.
To do this, first you must have python 3.x and python3-pip installed, then run these commands:

```
pip install virtualenv
python3 -m venv pwp
source pwp/bin/activate
```
Next, clone our project to your local machine and install the required extensions with:

```
git clone https://github.com/jkerola/coffee-api.git
cd coffee-api/
pip install -r requirements.txt
```
## Database Implementation
### Details
The database is SQLite3, though maybe changed for a PostgreSQL database later on. Models are accessed through SQLAlchemy ORM.
For a detailed view, check out *requirements.txt* for all used extensions.
### Unit tests
Unit tests are located in the *gcoffee/test/test_database.py* file.
To run the pre-written unit tests, simply run

```
pytest -s
```
in your terminal. The -s parameter tells pytest to print out our comments regarding the tests run.
### Manual testing
The project database is called *coffee.db*, found in the *gcoffee* folder.
For convenience, the database has been prepopulated with all tables.

To test the models and relationships yourself, open the Python interpreter with

```
python3
```
then run these commands to setup the database for inspection:

```python
from gcoffee import create_app, db
from gcoffee.models import User, Review, Batch, Coffee, Location
app = create_app()
context = app.app_context()
context.push()
# Run your database test, queries etc here
# When you are finished, simply run these commands to exit
context.pop()
exit()
```
For example, to create a new user, query and delete them afterwards:

```python
new_user = User(
    student_id=9999999
)
# student_id is a variable in the User class model and required for creation
# Commit this user to the database
db.session.add(new_user)
db.session.commit()

# Query user
user = User.query.filter_by(student_id=9999999).first()
# Delete User
db.session.delete(user)
```
For more details, check out *gcoffee/models.py* file for model defitions, or the wiki.

If you have any questions, send us a message!



### Authors
- [Janne Kerola](https://github.com/jkerola)
- [Fady Tawfeek](https://github.com/fadytawfeek)
- [Henry Laurila](https://github.com/hemeba47)
