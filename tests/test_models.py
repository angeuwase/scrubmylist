"""
This module contains unit tests for the database models.
"""


def test_user_model(new_user):
    """
    GIVEN a User model
    WHEN a new user object is instantiated
    THEN check that the user object has all the expected atrributes
    """
    assert new_user.email == 'test@gmail.com'
    assert new_user.hashed_password != 'password'
    assert new_user.date_registered.year == 2021
    assert new_user.date_registered.month == 4
    assert new_user.date_registered.day == 14
    assert new_user.is_confirmed == False
    assert new_user.date_confirmed == None
    assert new_user.date_updated == None
    assert new_user.is_admin == False

def test_new_password(new_user):
    """
    GIVEN a User model
    WHEN the user's password is changed
    THEN check that it has been changed to the new one
    """

    new_user.new_password('Anewpassword')

    assert new_user.email == 'test@gmail.com'
    assert new_user.hashed_password != 'Anewpassword'
    assert new_user.is_password_valid('Anewpassword') == True
    assert new_user.is_password_valid('password') == False



##### Main application functionality #####

def test_email_list_model(new_list):
    """
    GIVEN an EmailList model
    WHEN a new email list object is instantiated
    THEN check that the email list object has all the expected attributes
    """
    assert new_list.file_name == 'example.csv'
    assert new_list.date_uploaded.year == 2021
    assert new_list.date_uploaded.month == 4
    assert new_list.date_uploaded.day == 14
    assert new_list.owner_id == 17
    
