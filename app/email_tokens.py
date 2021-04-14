"""
Contains code for generating email confirmation tokens + checking that confirmation tokens are valid
"""

from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature
from flask import current_app, url_for

def generate_confirmation_email_token(user_email):
    """
    Given a user's email address, this function generates a URL safe token that will be included in the email link to be sent to the user to confirm their email
    """
    confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    confirm_url = url_for('auth.confirm_email',
                          token=confirm_serializer.dumps(user_email, salt='email-confirmation-salt'),
                          _external=True)
    return confirm_url