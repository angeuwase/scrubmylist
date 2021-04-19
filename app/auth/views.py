from . import auth_blueprint
from ..tasks import send_celery_email
from .forms import RegistrationForm, LoginForm
from flask import request, render_template, url_for, redirect, current_app, flash, abort
from datetime import datetime
from ..email_tokens import generate_confirmation_email_token
from .. import db
from ..models import User
from flask_login import current_user, login_required, logout_user, login_user
from urllib.parse import urlparse
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
   pass


@auth_blueprint.route('/password_reset')
def password_reset():
   pass