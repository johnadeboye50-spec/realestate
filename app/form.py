from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

def normalize_email(value):
    if value is None:
        return None
    return value.strip().lower()

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(check_deliverability=True, message='Please enter a valid email address')], filters=[normalize_email])
    role = RadioField('Account Type', 
                      choices=[('client', 'Client'), ('agent', 'Agent')],default='client', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    agree_terms = BooleanField('I agree to the Terms and Conditions', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), 
                                            Email(check_deliverability=True, message='Please enter a valid email address')], filters=[normalize_email])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EmailVerificationCodeForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify Email')