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