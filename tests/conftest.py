import pytest
from app import db, create_app, celery
from app.models import User, EmailList, ValidationResult
from datetime import datetime
import os
import io
import requests


@pytest.fixture(scope='module')
def new_user():
    """
    This fixture creates an object of the User class. 
    It is used to test that when a new user is instantiated, the user object has all the expected attributes.

    Expected attributes of a user:
    1. id 
    2. email address
    3. hashed_password
    4. date_registered 
    5. is_confirmed (default is False)
    6. date_confirmed (default is None)
    7. date_updated (default is None)
    8. is_admin (default is False)
    """
    user = User('test@gmail.com', 'password', date_registered=datetime(2021,4,14))
    return user


@pytest.fixture(scope='module')
def test_client():
    """
    This fixture is used by all the tests.
    It creates a flask application configured for testing, and uses it to create a test client that can be used to send requests to the application for testing purposes.
    Since it is accessible by all tests, the code for initialising the database is also placed in here to be used by the tests that require it.
    """

    test_app = create_app()
    test_app.config.from_object('config.TestingConfig')
    celery.conf.task_always_eager = True
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            db.create_all()
            yield testing_client
            with test_app.app_context():
                db.drop_all()

@pytest.fixture(scope='module')
def register_default_user(test_client):
    """
    This fixture registers a default user.
    It will be used to test user management functionality that requires a registered user, such as login/logout, 
    """

    test_client.post('/register', data={
        'email': 'default@gmail.com',
        'password': 'password',
        'confirm_password': 'password'
    },follow_redirects=True)

    return 


@pytest.fixture(scope='function')
def login_default_user(test_client, register_default_user):
    """
    This fixture logs in the default user, yields for testing to occur, and then logs the user out once testing is completed
    It will be used to test functionality that requires a logged-in user.
    """
    #log in the default user
    test_client.post('login', data={
        'email': 'default@gmail.com',
        'password': 'password'}, follow_redirects=True )

    yield # this is where testing occurs

    test_client.get('/logout', follow_redirects=True)


@pytest.fixture(scope='function')
def confirm_default_user_email(test_client, login_default_user):
    """
    This fixture logs the default user in, marks them as having confirmed their email address so that the password reset and profile functionality can be tested.
    After testing is completed the user's email is marked as unconfirmed again to return the system to a known state.
    """

    user = User.query.filter_by(email='default@gmail.com').first()

    user.is_confirmed = True
    user.date_confirmed = datetime(2021, 4, 20)
    user.date_updated = datetime(2021, 4, 20)
    db.session.add(user)
    db.session.commit()


@pytest.fixture(scope='function')
def reset_default_user_to_original():
    """
    The tests that test password reset and email confirmation functionality can change the attributes of the default user.
    This fixture is required to make sure that the default user's attributes always returns back to the default values.
    """
    yield  # this is where the testing happens!

    user = User.query.filter_by(email='default@gmail.com').first()
    user.is_confirmed = False
    user.date_confirmed = None
    user.date_updated = None
    user.new_password('password')
    db.session.add(user)
    db.session.commit()


##### Main application functionality #####

@pytest.fixture(scope='module')
def new_list():
    """
    This fixture creates an object of the EmailList class. 
    It is used to test that when a new list object is instantiated, the object has all the expected attributes.

    Expected attributes of a user:
    1. id 
    2. file name
    2. owner_id
    3. total_emails
    2. total_unique_emails
    3. date_uploaded

    """
    email_list = EmailList('example.csv',17, 10, 8, date_uploaded=datetime(2021,4,14))
    return email_list

@pytest.fixture(scope='function')
def new_validation_result():
    """
    This fixture creates an object of the ValidationResult class.
    It is used to test the functionality of retrieving and storing email validation results.

    Expected attributes of a ValidationResult object:
    1. id
    2. email_address
    3. email_list_id 
    4. is_free
    5. is_syntax
    6. is_domain
    7. is_smtp
    8. is_verified
    9. is_server_down
    10. is_greylisted
    11. is_disposable
    12. is_suppressed
    13. is_role
    14. is_high_risk
    15. is_catchall
    16. status
    17. mailboxvalidator_score
    """  
    #new_result = ValidationResult('test_email@gmail.com', 17, True, True, True, True, True, False, False, False, False, False, False, False, True, '0.58')
    new_result = ValidationResult('test_email@gmail.com', 17)

    return new_result


@pytest.fixture(scope='function')
def delete_uploaded_file():
    yield # this is where testing occurs

    # delete the csv file saved to the assets folder during a test
    os.remove(os.path.join('assets', 'default@gmail.com subscribers.csv'))
    emaillists = EmailList.query.all()
    for emaillist in emaillists:
        db.session.delete(emaillist)
        db.session.commit()

@pytest.fixture(scope='function')
def upload_email_list_for_default_user(test_client, login_default_user):
    """
    This fixture uploads a csv file for the default user
    """
    csv_file_data = b'id,first_name,last_name,email,gender,ip_address\r\n1,Rolland,Rosario,rrosario0@wufoo.com,Polygender,177.238.45.164\r\n2,Hollyanne,Duding,hduding1@webeden.co.uk,Bigender,216.222.232.126\r\n3,Masha,Mott,mmott2@microsoft.com,Agender,132.92.237.89\r\n4,Kathe,Casford,kcasford3@miibeian.gov.cn,Male,8.54.243.37\r\n5,Raquel,Mulford,rmulford4@deliciousdays.com,Polygender,71.255.133.255\r\n6,Pierce,Wyard,pwyard5@fema.gov,Non-binary,214.115.254.74\r\n7,Lisbeth,Kuhnwald,lkuhnwald6@indiatimes.com,Female,96.42.27.204\r\n8,Aubine,Leyson,aleyson7@mozilla.org,Female,35.27.8.150\r\n9,Melba,Pellett,mpellett8@istockphoto.com,Bigender,58.174.243.218\r\n10,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n11,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n12,Victoria,Fransman,vfransman9@boston.com,Male,231.235.151.181\r\n'

    data = dict(csv_file=(io.BytesIO(csv_file_data), "subscribers.csv"))

    test_client.post('/upload_email_list', 
                               data=data,
                               content_type='multipart/form-data', 
                               follow_redirects=True)


########################
#### Helper Classes ####
########################

class MockSuccessResponse(object):
    def __init__(self, url):
        self.status_code = 200
        self.url = url
        self.headers = {'Email_Validator': 'MailboxValidator'}

    def json(self):
        return {
    "email_address": "test_email@gmail.com",
    "domain": "gmail.com",
    "is_free": "True",
    "is_syntax": "True",
    "is_domain": "True",
    "is_smtp": "True",
    "is_verified": "True",
    "is_server_down": "False",
    "is_greylisted": "False",
    "is_disposable": "False",
    "is_suppressed": "False",
    "is_role": "False",
    "is_high_risk": "True",
    "is_catchall": "False",
    "mailboxvalidator_score": "0.45",
    "time_taken": "0.8784",
    "status": "False",
    "credits_available": 999999999,
    "error_code": "",
    "error_message": ""
}

class MockFailedResponse(object):
    def __init__(self, url):
        self.status_code = 404
        self.url = url
        self.headers = {'Email_Validator': 'MailboxValidator'}

    def json(self):
        return {
            'email_address': '', 
            'domain': '', 
            'is_free': '', 
            'is_syntax': '', 
            'is_domain': '', 
            'is_smtp': '', 
            'is_verified': '', 
            'is_server_down': '', 
            'is_greylisted': '', 
            'is_disposable': '', 
            'is_suppressed': '', 
            'is_role': '', 
            'is_high_risk': '', 
            'is_catchall': '', 
            'mailboxvalidator_score': '', 
            'time_taken': 0.0031, 
            'status': '', 
            'credits_available': '', 
            'error_code': '104', 
            'error_message': 'Insufficient credits.'}

@pytest.fixture(scope='function')
def mock_requests_get_success(monkeypatch):

    def mock_get(url):
        return MockSuccessResponse(url)

    url = 'https://api.mailboxvalidator.com/v1/validation/single?email=test_email@gmail.com&key=TCLVR8EZUUAAKLXKX0FI&format=json'
    
    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture(scope='function')
def mock_requests_get_failure(monkeypatch):

    def mock_get(url):
        return MockFailedResponse(url)

    url = 'https://api.mailboxvalidator.com/v1/validation/single?email=test_email@gmail.com&key=TCLVR8EZUUAAKLXKX0FI&format=json'
    
    monkeypatch.setattr(requests, 'get', mock_get)