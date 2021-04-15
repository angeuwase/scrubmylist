"""
This module contains functionality tests for the auth blueprint (user management)
"""

from app import mail
import pytest

@pytest.mark.registration
def test_get_registration_form(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/register' is received
    THEN check that the registration form renders correctly
    """

    response = test_client.get('/register', follow_redirects=True)

    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Confirm Password' in response.data

@pytest.mark.registration
@pytest.mark.parametrize('email, password, confirm_password', [('', 'password', 'password'),('test@gmail.com', '', 'password'),('test@gmail.com', 'password', ''),('', '', 'password'), ('', 'password', ''),('test@gmail.com', '', '') ,('', '', ''), ('test@gmail.com', 'password123', 'password')])
def test_invalid_registration_missing_fields(test_client, email, password, confirm_password):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received but there is a missing field(s) or the passwords dont match
    THEN check that the user is told to fix the errors
    """
    
    response = test_client.post('/register', data={'email': email, 'password': password, 'confirm_password': confirm_password}, follow_redirects=True)

    assert response.status_code ==200
    assert b'Register' in response.data
    assert b'Error in form data!' in response.data

@pytest.mark.registration
def test_invalid_registration_existing_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received from an existing user
    THEN check that the user is redirected to the login page and told to login
    """
    
    test_client.post('/register', data={'email': 'test@gmail.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    response = test_client.post('/register', data={'email': 'test@gmail.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)

    print(response.data.decode())

    assert response.status_code ==200
    assert b'Login' in response.data
    assert b'You already have an account! Please login.' in response.data
    
@pytest.mark.registration
def test_successful_registration_new_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received from a new user 
    THEN check that the user is added to the database, sent a confirmation email and redirected to the login page to sign in. 
    """
    

    with mail.record_messages() as outbox:

        response = test_client.post('/register', data={'email': 'test2@gmail.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)

        assert response.status_code ==200
        assert b'Login' in response.data
        assert b'Thanks for registering! Please check your email to confirm your email address. In the meantime, sign in to access your account.' in response.data
        assert len(outbox) == 1
        assert outbox[0].subject == 'Flask App - Confirm Your Email Address' 
        assert outbox[0].sender == 'angeapptesting18'
        assert outbox[0].recipients[0] == 'test2@gmail.com'
        assert 'http://localhost/confirm_email/' in outbox[0].html 


@pytest.mark.login
def test_get_login_form(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/login' is received 
    THEN check that the login form renders correctly
    """

    response = test_client.get('/login', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Forgot your password?' in response.data

@pytest.mark.login
@pytest.mark.parametrize('email, password', [('unregistered@gmail.com', 'password'),('default@gmail.com', 'wrong_password')])
def test_unsuccessful_login_unregistered_user_and_incorrect_password(test_client, register_default_user, email, password):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from an unregistered user or registered user with incorrect password
    THEN check that they are told 'credentials not recognised'
    """

    response = test_client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Forgot your password?' in response.data
    assert b'Credentials not recognised! Please check your email and password. If you arent a registered user, you need to first create an account!' in response.data


