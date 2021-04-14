from . import auth_blueprint
from ..tasks import send_celery_email
from .forms import RegistrationForm
from flask import request, render_template, url_for, redirect, current_app, flash
from datetime import datetime
from ..email_tokens import generate_confirmation_email_token
from .. import db
from ..models import User
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

        flash('Error in form data!')

        

    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login')
def login():
    return render_template('auth/login.html')

@auth_blueprint.route('/confirm_email/<token>')
def confirm_email(token):
   pass