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
    assert b'Error in form!' in response.data

@pytest.mark.registration
def test_invalid_registration_existing_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received from an existing user
    THEN check that the user is redirected to the login page and told to login
    """
    
    test_client.post('/register', data={'email': 'test@gmail.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    response = test_client.post('/register', data={'email': 'test@gmail.com', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)

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
def test_unsuccessful_login_unregistered_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from an unregistered user or registered user with incorrect password
    THEN check that they are told 'credentials not recognised'
    """

    response = test_client.post('/login', data={'email': 'unregistered@gmail.com', 'password': 'password'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Forgot your password?' in response.data
    assert b'Credentials not recognised! Please check your email and password. If you arent a registered user, you need to first create an account!' in response.data


@pytest.mark.login
def test_unsuccessful_login_incorrect_password(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from an unregistered user or registered user with incorrect password
    THEN check that they are told 'credentials not recognised'
    """

    response = test_client.post('/login', data={'email': 'default@gmail.com', 'password': 'wrong_password'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Forgot your password?' in response.data
    assert b'Credentials not recognised! Please check your email and password. If you arent a registered user, you need to first create an account!' in response.data


@pytest.mark.login
def test_successful_login_and_logout(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from a registered user with valid credentials
    THEN check that they are logged in successfully and redirected to the profile page and that the navbar is appropriate
    """

    response = test_client.post('/login', data={'email':'default@gmail.com', 'password':'password'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data

    """
    GIVEN a flask application
    WHEN a GET request is received for '/logout' from a logged in user
    THEN check that they are logged out successfully and redirected to the homme page and that the navbar is appropriate
    """

    response = test_client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' not in response.data
    assert b'You have been successfully logged out!' in response.data

@pytest.mark.login
def test_login_valid_next_path(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from a registered user with valid credentials with a valid relative path in the query 
    THEN check that the user is redirected to the requested page after successfully logging in

    Note: the addresses of any web pages of the web application will always be given as relative paths as they live on the same server as the login page. 
    """

    response = test_client.post('/login?next=%2Fprofile', data={'email': 'default@gmail.com', 'password': 'password'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' in response.data

    # Log out the user - Clean up! Otherwise next next will fail with "already logged in" response
    test_client.get('/logout', follow_redirects=True)


@pytest.mark.login
def test_login_invalid_next_path(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from a registered user with valid credentials with an invalid full path in the query 
    THEN check that a Bad Request (400) error is raised

    Note: the address of external sites will always be given as a full path because it requires the user to exit the web application and go elsewhere.
    """

    response = test_client.post('/login?next=http://www.unsafesite.com', data={'email': 'default@gmail.com', 'password': 'password'}, follow_redirects=True)

    print(response.data.decode())

    assert response.status_code == 400
    assert b'Bad Request' in response.data


@pytest.mark.login
def test_login_when_already_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' from a logged in user
    THEN check that the user is told that they are already logged in
    """

    response = test_client.post('login', data={
        'email': 'default@gmail.com',
        'password': 'password'}, follow_redirects=True )

    assert response.status_code == 200
    assert b'You are already logged in!' in response.data

@pytest.mark.login
def test_logout_when_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/logout' from a user that is not logged in
    THEN check that they are redirected to the login page. Only logged in users can access the '/logout' route
    """

    # make sure no user is logged in 
    test_client.get('/logout', follow_redirects=True)

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page.' in response.data


@pytest.mark.login
def test_post_request_for_logout(test_client):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/logout' 
    THEN check that it raises the method not allowed (405) error
    """

    response = test_client.post('/logout', follow_redirects=True)

    assert response.status_code == 405
    assert b'Method Not Allowed' in response.data




    