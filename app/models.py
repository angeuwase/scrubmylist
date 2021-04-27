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
    uploaded_lists = db.relationship('EmailList', backref='owner', lazy='dynamic')


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


class EmailList(db.Model):
    """
    This class maps to the email lists table in the database.

    Attributes of interest for a given email list:
    1. id (integer)
    2. file_name (string) - the name of the csv file uploaded by the user
    3. owner_id (integer) - the id of the user who uploaded the email list
    4. total_emails (integer) - the count of all the emails in the email list
    5. total_unique_emails (integer) - the count of all unique emails in the email list (duplicates removed)
    6. date_uploaded (datetime) - the date the user uploaded the email list
    7. is_validated (bool) - whether or not the email list has been verified
    8. date_verified (datetime) - the date that the email list was verified
    9. validation_result 
    
    """
    __tablename__ = 'emaillists'

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    total_emails = db.Column(db.Integer)
    total_unique_emails = db.Column(db.Integer)
    date_uploaded = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean)
    date_verified = db.Column(db.DateTime)
    validation_results = db.relationship('ValidationResult', backref='parent_list', lazy='dynamic')
    

    def __init__(self, file_name: str, owner_id: int, total_emails: int, total_unique_emails: int, date_uploaded=None):
        self.file_name = file_name
        self.owner_id = owner_id
        self.total_emails = total_emails
        self.total_unique_emails = total_unique_emails
        self.date_uploaded = date_uploaded
        


    def __repr__(self):
        return '<Email List {}>'.format(self.id)


class ValidationResult(db.Model):
    """
    This class maps to the validation results table in the database

    Attributes of interest for a given validation result:
    1. id
    2. email_address 
    3. email_list_id - the id of the email_list that the email belongs to
    4. is_free (bool) - Whether the email address is from a free email provider like Gmail or Hotmail.
    5. is_syntax (bool) - Whether the email address is syntactically correct.
    6. is_domain (bool) - Whether the email address has a valid MX record in its DNS entries.
    7. is_smtp (bool) - Whether the mail servers specified in the MX records are responding to connections.
    8. is_verified (bool) - Whether the mail server confirms that the email address actually exist.
    9. is_server_down (bool) - Whether the mail server is currently down or unresponsive.
    10. is_greylisted (bool) - Whether the mail server employs greylisting where an email has to be sent a second time at a later time
    11. is_disposable (bool) - Whether the email address is a temporary one from a disposable email provider.
    12. is_suppressed (bool) - Whether the email address is in our blacklist.
    13. is_role (bool) - 	Whether the email address is a role-based email address like admin@example.net or webmaster@example.net.
    14. is_high_risk (bool) - Whether the email address contains high risk keywords
    15. is_catchall (bool) - Whether the email address is a catch-all address.
    16. status (bool) - Whether the email address is valid based on all the previous fields.
    17. mailboxvalidator_score (string) - Email address reputation score. Score > 0.70 means good; score > 0.40 means fair; score ≤ 0.40 means poor.
    """

    __tablename__ = 'validationresults'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String)
    email_list_id = db.Column(db.Integer, db.ForeignKey('emaillists.id'))
    is_free = db.Column(db.Boolean)
    is_syntax = db.Column(db.Boolean)
    is_domain = db.Column(db.Boolean)
    is_smtp = db.Column(db.Boolean)
    is_verified = db.Column(db.Boolean)
    is_server_down = db.Column(db.Boolean)
    is_greylisted = db.Column(db.Boolean)
    is_disposable = db.Column(db.Boolean)
    is_suppressed = db.Column(db.Boolean)
    is_role = db.Column(db.Boolean)
    is_high_risk = db.Column(db.Boolean)
    is_catchall = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    mailboxvalidator_score = db.Column(db.String)

    def __init__(self, email_address,email_list_id,is_free,is_syntax,is_domain,is_smtp,is_verified,is_server_down,is_greylisted,is_disposable,is_suppressed,is_role,is_high_risk,is_catchall,status,mailboxvalidator_score):
        self.email_address = email_address
        self.email_list_id = email_list_id
        self.is_free = is_free
        self.is_syntax = is_syntax
        self.is_domain = is_domain
        self.is_smtp = is_smtp
        self.is_verified = is_verified
        self.is_server_down = is_server_down
        self.is_greylisted = is_greylisted
        self.is_disposable = is_disposable
        self.is_suppressed = is_suppressed
        self.is_role = is_role
        self.is_high_risk = is_high_risk
        self.is_catchall = is_catchall
        self.status = status
        self.mailboxvalidator_score = mailboxvalidator_score 
    
    def __repr__(self):
        return '<Validation Result {0}: {1}>'.format(self.id, self.email_address)

    