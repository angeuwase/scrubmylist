from . import auth_blueprint
from ..tasks import send_celery_email
from .forms import RegistrationForm, LoginForm, PasswordResetViaEmailForm, PasswordForm
from flask import request, render_template, url_for, redirect, current_app, flash, abort
from datetime import datetime
from ..email_tokens import generate_confirmation_email_token, generate_password_reset_token
from .. import db
from ..models import User
from flask_login import current_user, login_required, logout_user, login_user
from urllib.parse import urlparse
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature

#@auth_blueprint.route('/register/<email>')
#def test_register(email):
    #message_data = {
        #'subject': 'Hello from Flask',
       # 'body': 'This email was send asynchronously using celery',
       # 'recipients': email
   # }

   # send_celery_email.apply_async(args=[message_data])

    #return 'Hello world from the auth blueprint'

@auth_blueprint.route('/register', methods = ['GET', 'POST'])
def register():

    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            # Check if the email given in the registration form is already in the database
            user = User.query.filter_by(email=form.email.data).first()

            # If registration form is received from an existing user, reject it
            if user:
                flash('You already have an account! Please login.')
                return redirect(url_for('auth.login'))

            # Create new user object and add new user to the database
            new_user = User(form.email.data, form.password.data, date_registered=datetime.now())
            db.session.add(new_user)
            db.session.commit()
    
            current_app.logger.info('A new user has been added: {}'.format(new_user.email))

            # Send account confirmation email
            token = generate_confirmation_email_token(new_user.email)
            message_data = {
                'subject': 'Flask App - Confirm Your Email Address',
                'recipients': new_user.email,
                'html': render_template('auth/email_confirmation.html', confirm_url=token)
            }

            send_celery_email.apply_async(args=[message_data])

            flash('Thanks for registering! Please check your email to confirm your email address. In the meantime, sign in to access your account.')
            return redirect(url_for('auth.login'))

        flash('Error in form!')
    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # Don't let a logged in user log in again
    if current_user.is_authenticated:
        flash('You are already logged in!')
        current_app.logger.info(f'Duplicate login attempt by user: {current_user.email}')
        return redirect(url_for('auth.profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            user = User.query.filter_by(email=form.email.data).first()

            if user and user.is_password_valid(form.password.data):
                login_user(user)
                current_app.logger.info(f'Successful login: {current_user.email}')

                # If the next URL is not specified, redirect the user to the profile page
                if not request.args.get('next'):
                    return redirect(url_for('auth.profile'))

                # If the next URL is specified, check whether it is a relative path (valid) or a full path (invalid). 
                # Redirect user if it's valid otherwise raise a bad request error
                next_url = request.args.get('next')
                if urlparse(next_url).scheme != '' or urlparse(next_url).netloc != '':
                    current_app.logger.info(f'Invalid next path in login request: {next_url}')
                    logout_user()
                    return abort(400)

                current_app.logger.info(f'Valid next path in login request: {next_url}')
                return redirect(next_url)

        
        flash('Credentials not recognised! Please check your email and password. If you arent a registered user, you need to first create an account!')
    
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    current_app.logger.info(f'Logout by user: {current_user.email}')
    logout_user()
    flash('You have been successfully logged out!')
    return redirect(url_for('main.index'))

@auth_blueprint.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')


@auth_blueprint.route('/confirm_email/<token>')
def confirm_email(token):

    try:
        confirm_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except BadSignature as e:
        flash('The confirmation link is invalid or has expired.')
        current_app.logger.info(f'Invalid or expired confirmation link received from IP address: {request.remote_addr}')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if user.is_confirmed:
        flash('Account already confirmed. Please login.')
        current_app.logger.info(f'Confirmation link received for a confirmed user: {user.email}')
    else:
        user.is_confirmed = True
        user.date_confirmed = datetime.now()
        user.date_updated = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!')
        current_app.logger.info(f'Email address confirmed for: {user.email}')

    return redirect(url_for('main.index'))


@auth_blueprint.route('/password_reset_via_email', methods=['GET', 'POST'])
def password_reset_via_email():
    form = PasswordResetViaEmailForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            

            if not user: 
                flash('Cannot send password reset link. The email address provided is either unregistered or has not yet been confirmed.')
                current_app.logger.info(f'Password reset request received for unregistered user: {form.email.data}')
                return redirect(url_for('auth.login'))
            else:
                if user.is_confirmed == False:
                    flash('Cannot send password reset link. The email address provided is either unregistered or has not yet been confirmed.')
                    current_app.logger.info(f'Password reset request received for unconfirmed email address: {user.email}')
                    return redirect(url_for('auth.login'))
                else:
                    token = generate_password_reset_token(user.email)
                    message_data = {
                                    'subject': 'Flask App - Password Reset',
                                    'recipients': user.email,
                                    'html': render_template('auth/password_reset_email.html', reset_url=token)
                                }

                    send_celery_email.apply_async(args=[message_data])

                    flash('Please check your email for a password reset link.')
                    current_app.logger.info(f'Password reset link emailed to user: {user.email}')
                    return redirect(url_for('auth.login'))
        
        flash('Error in form!')
                
    return render_template('auth/password_reset_via_email.html', form=form)
   
@auth_blueprint.route('/password_reset_via_token/<token>', methods=['GET', 'POST'])
def password_reset_via_token(token):
    try:
        reset_serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = reset_serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except BadSignature as e:
        flash('The password reset link is invalid or has expired.')
        return redirect(url_for('auth.login'))

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if user is None:
            flash('Invalid email address!')
            return redirect(url_for('auth.login'))

        user.new_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your password has been updated!')
        return redirect(url_for('auth.login'))

    return render_template('auth/password_reset_with_token.html', form=form)