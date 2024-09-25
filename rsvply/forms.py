from collections.abc import Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
      IntegerField, TimeField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange
import email_validator
from rsvply.models import User


from datetime import datetime
import pytz
ist_timezone = pytz.timezone('Asia/Kolkata')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(), Length(min=10, max=20)])
    date = DateField('Date', format="%Y-%m-%d", validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])

    start_time = TimeField('Start', validators=[DataRequired()])
    end_time = TimeField('End', validators=[DataRequired()])



    location = StringField('Location',validators=[DataRequired(), Length(min=10,max=100)])
    submit = SubmitField('Generate Form')
    # expire link by

    def validate_date(self, date):
        today_date = datetime.now(ist_timezone).date()
        if date.data < today_date:
            raise ValidationError('Cannot choose dates from the past')
    


