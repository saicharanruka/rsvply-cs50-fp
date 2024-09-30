from collections.abc import Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,\
      IntegerField, TimeField, DateField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError, NumberRange
import email_validator
from rsvply.models import User


from datetime import datetime
from rsvply import IST

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
    title = StringField('Title',validators=[DataRequired(), Length(min=5, max=30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=20)])

    date = DateTimeField('Date',format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    expiry = DateTimeField('Expiry',format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    location = StringField('Location',validators=[DataRequired(), Length(min=10,max=100)])
    submit = SubmitField('Generate')

    def validate_date(self, date):
        today_date = datetime.now(IST)
        input_date = date.data.astimezone(IST)
        if input_date < today_date:
            raise ValidationError('Cannot choose date and time from the past')
        
    
    def validate_expiry(self, field):
        date = self.date.data.astimezone(IST)
        expiry = field.data.astimezone(IST)
        today = datetime.now(IST)

        if expiry < today:
            raise ValidationError("Expiry date and time must be after today.")
        if expiry > date:
            raise ValidationError("Expiry date and time must be before the event.")


class RSVPForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])

    attending = BooleanField('RSVP ?')
    submit = SubmitField('Submit')
