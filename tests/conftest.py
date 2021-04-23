import pytest
from app import db, create_app, celery
from app.models import User, EmailList
from datetime import datetime
import os


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
    2. file_name
    3. date_uploaded
    4. owner_id

    """
    email_list = EmailList('example.csv',17, date_uploaded=datetime(2021,4,14))
    return email_list


@pytest.fixture(scope='function')
def delete_uploaded_file():
    yield # this is where testing occurs

    # delete the csv file saved to the assets folder during a test
    os.remove(os.path.join('assets', 'default@gmail.com subscribers.csv'))


