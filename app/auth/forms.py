from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match'), Length(min=6, max=120)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=120)])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=120)])

class PasswordResetViaEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class PasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match'), Length(min=6, max=120)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=120)])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password: ', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_new_password', message='Passwords must match'), Length(min=6, max=120)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6, max=120)])