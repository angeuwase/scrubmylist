import pytest
from app import db, create_app, celery
from app.models import User
from datetime import datetime


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

