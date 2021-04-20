from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    """
    This class maps to a users table in the database.

    Users' attributes that are of interest:
    1. id 
    2. email address - email address of the user
    3. hashed_password - hashed password
    4. date_registered - date & time that the user registered
    5. is_confirmed (default is False) - flag indicating if the user's email address has been confirmed
    6. date_confirmed (default is None) - date & time that the user's email address was confirmed
    7. date_updated (default is None) - flag indicating if the user has recently changed their details (such as password)
    8. is_admin (default is False) - flag indicating if the user has admin rights

    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    hashed_password = db.Column(db.String)
    date_registered = db.Column(db.DateTime)
    is_confirmed = db.Column(db.Boolean, default=False)
    date_confirmed = db.Column(db.DateTime)
    date_updated = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)


    def __init__(self, email: str, password_plaintext: str, date_registered=None, is_admin=False):
        """Create a new User object

        This constructor assumes that an email is sent to the new user to confirm
        their email address at the same time that the user is registered.
        """
        self.email = email
        self.hashed_password = generate_password_hash(password_plaintext)
        self.date_registered = date_registered
        self.is_confirmed = False
        self.date_confirmed = None
        self.date_updated = None
        self.is_admin = is_admin


    def is_password_valid(self, password_plaintext: str):
        return check_password_hash(self.hashed_password, password_plaintext)

    def new_password(self, password_plaintext: str):
        self.hashed_password = generate_password_hash(password_plaintext)
        self.date_updated =  datetime.now()


    def __repr__(self):
        return '<User {0}: {1}>'.format(self.id, self.email)