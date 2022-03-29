from datetime import datetime
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from flask_wtf.file import FileAllowed , FileField , FileRequired
from flask_wtf import FlaskForm
from wtforms.validators  import DataRequired , Email , EqualTo , ValidationError

from ecomfinal.customers.models import CustomerRegister

class Customer(FlaskForm):
    name = StringField("Username" , validators=[DataRequired()])
    city = StringField('City' , validators=[DataRequired()])
    country = StringField('Country' , validators=[DataRequired()])
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm' , message = 'Both passwords must match')])
    confirm = PasswordField('Confirm Password' , validators=[DataRequired()])
    date_created = StringField('Date Created' , default=datetime.utcnow)
    zip_code = StringField('Zip code' , validators=[DataRequired()])
    address = StringField('Address' , validators=[DataRequired()])
    profile = FileField('Profile Image' , validators = [FileAllowed(['jpg' , 'png' , 'jpeg' , 'gif'])])
    submit = SubmitField('Submit')
class Login(FlaskForm):
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password',validators=[DataRequired()])

class UpdateAccountForm(FlaskForm):
    name = StringField('Username' , validators = [DataRequired()])
    city = StringField('City' , validators=[DataRequired()])
    country = StringField('Country' , validators=[DataRequired()])
    date_created = StringField('Date Created' , default=datetime.utcnow)
    zip_code = StringField('Zip code' , validators=[DataRequired()])
    profile = FileField('Profile Image' , validators = [FileAllowed(['jpg' , 'png' , 'jpeg' , 'gif'])])
    address = StringField('Address' , validators=[DataRequired()])
    email = StringField('Email' , validators = [DataRequired() , Email()])
    submit = SubmitField('Update')

    def validate_username(self , name):
        if name.data != current_user.name:
            user = CustomerRegister.query.filter_by(username=name.data).first()
            if user:
                raise ValidationError('That username is already taken.Please choose a different one')

   
    def validate_email(self , email):
        if email.data != current_user.email:
            user = CustomerRegister.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken.Please choose a different one')

class CustomerLoginForm(FlaskForm):
    email = StringField('emailAddress' , validators = [DataRequired()])
    password = PasswordField('Password' , validators = [DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')