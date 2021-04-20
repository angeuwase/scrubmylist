"""
This module contains functionality tests for the auth blueprint (user management)
"""

from app import mail
import pytest
from app.email_tokens import generate_confirmation_email_token
from app.models import User
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
import time 

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


@pytest.mark.account_confirmation
def test_email_confirmation_valid_link(test_client, register_default_user, reset_default_user_to_original):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/confirm_email/<token>' route from a valid link
    THEN check that the user's email address is marked as confirmed
    """
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = confirm_serializer.dumps('default@gmail.com', salt='email-confirmation-salt')

    response = test_client.get('/confirm_email/'+token, follow_redirects=True)

    assert response.status_code == 200
    assert b'Thank you for confirming your email address!' in response.data
    user = User.query.filter_by(email='default@gmail.com').first()
    assert user.is_confirmed == True

@pytest.mark.account_confirmation
def test_email_confirmation_valid_link_confirmed_user(test_client, register_default_user, reset_default_user_to_original):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/confirm_email/<token>' route from a valid link from an already confirmed user
    THEN check that the user gets a message indicating that their email address has already been confirmed
    """
    

    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = confirm_serializer.dumps('default@gmail.com', salt='email-confirmation-salt')

    test_client.get('/confirm_email/'+token, follow_redirects=True)

    response = test_client.get('/confirm_email/'+token, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account already confirmed.' in response.data
    user = User.query.filter_by(email='default@gmail.com').first()
    assert user.is_confirmed == True

@pytest.mark.account_confirmation
def test_email_confirmation_invalid_link(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/confirm_email/<token>' route from an invalid link
    THEN check that an error message is displayed to the user
    """

    response = test_client.get('/confirm_email/a_bad_token', follow_redirects=True)

    assert response.status_code == 200
    assert b'The confirmation link is invalid or has expired.' in response.data


@pytest.mark.password_reset
def test_get_password_reset_via_email_form(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/password_reset_via_email' route (ie when a user clicks on the 'forgot your password?' link on the login form)
    THEN check that the password_reset_via_email form is successfully returned
    """

    response = test_client.get('/password_reset_via_email', follow_redirects=True)

    assert response.status_code == 200
    assert b'Password Reset' in response.data
    assert b'Please enter your email' in response.data
    assert b'Email' in response.data
    assert b'Submit' in response.data


@pytest.mark.password_reset
def test_post_password_reset_via_email_form_unregistered_email(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for the '/password_reset_via_email' route with an unregistered email or a registered email address that has not been confirmed yet
    THEN check that an error message is flashed and no password_reset email is sent
    """
    with mail.record_messages() as outbox:

        response = test_client.post('/password_reset_via_email',
                                    data={'email': 'unregistered@gmail.com'},
                                    follow_redirects=True)
        
        assert response.status_code == 200
        assert len(outbox) == 0
        assert b'Cannot send password reset link. The email address provided is either unregistered or has not yet been confirmed.' in response.data


@pytest.mark.password_reset
def test_post_password_reset_via_email_form_unconfirmed_email(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for the '/password_reset_via_email' route with an unregistered email or a registered email address that has not been confirmed yet
    THEN check that an error message is flashed and no password_reset email is sent
    """
    with mail.record_messages() as outbox:

        response = test_client.post('/password_reset_via_email',
                                    data={'email': 'default@gmail.com'},
                                    follow_redirects=True)
        
        assert response.status_code == 200
        assert len(outbox) == 0
        assert b'Cannot send password reset link. The email address provided is either unregistered or has not yet been confirmed.' in response.data
 

@pytest.mark.password_reset
def test_post_password_reset_via_email_form_confirmed_email(test_client, confirm_default_user_email, reset_default_user_to_original):
    """
    GIVEN a flask application
    WHEN a POST request is received for the '/password_reset_via_email' route with a confirmed email address 
    THEN check that an email with a password reset link was queued up to be sent
    """
    with mail.record_messages() as outbox:

        response = test_client.post('/password_reset_via_email',
                                    data={'email': 'default@gmail.com'},
                                    follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Please check your email for a password reset link.' in response.data
        assert len(outbox) == 1
        assert outbox[0].subject == 'Flask App - Password Reset'
        assert outbox[0].recipients[0] == 'default@gmail.com'
        assert 'http://localhost/password_reset_via_token/' in outbox[0].html


@pytest.mark.password_reset
def test_get_password_reset_form_valid_link(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/password_reset_via_token/<token>' route from a valid link
    THEN check that the password reset form is rendered correctly
    """
    reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = reset_serializer.dumps('default@gmail.com', salt='password-reset-salt')

    response = test_client.get('/password_reset_via_token/'+token, follow_redirects=True)

    assert response.status_code == 200
    assert b'Password Reset' in response.data
    assert b'New Password' in response.data
    assert b'Confirm Password' in response.data
    assert b'Submit' in response.data

@pytest.mark.password_reset
def test_get_password_reset_form_invalid_link(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for the '/password_reset_via_token/<token>' route from an invalid link
    THEN check that an error message is displayed
    """

    response = test_client.get('/password_reset_via_token/a_bad_token', follow_redirects=True)

    assert response.status_code == 200
    assert b'The password reset link is invalid or has expired.' in response.data

@pytest.mark.password_reset
def test_post_password_reset_form_valid_link(test_client, reset_default_user_to_original):
    """
    GIVEN a flask application
    WHEN a POST request is received for the '/password_reset_via_token/<token>' route from a valid link
    THEN check that the user's password gets reset
    """
    reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = reset_serializer.dumps('default@gmail.com', salt='password-reset-salt')

    response = test_client.post('/password_reset_via_token/'+token,
                                data={'password':'newpassword', 'confirm_password':'newpassword'},
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Your password has been updated!' in response.data

@pytest.mark.password_reset
def test_post_password_reset_form_invalid_link(test_client):
    """
    GIVEN a flask application
    WHEN a POST request is received for the '/password_reset_via_token/<token>' route from an invalid link
    THEN check that an error message gets shown
    """
    token = 'a bad token'

    response = test_client.post('/password_reset_via_token/'+token,
                                data={'password':'newpassword', 'confirm_password':'newpassword'},
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Your password has been updated!' not in response.data
    assert b'The password reset link is invalid or has expired.' in response.data