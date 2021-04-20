"""
Contains code for generating email confirmation tokens + checking that confirmation tokens are valid
"""

from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask import current_app, url_for

def generate_confirmation_email_token(user_email):
    """
    Given a user's email address, this function generates a unique URL to be sent to the user to confirm their email. 
    The serializer object encodes the user's email address and a timestamp into a token. 
    The url_for function generates a unique url from the endpoint and the token
    """
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('auth.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True)
    return confirm_url