from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField , PasswordField , BooleanField , IntegerField , TextAreaField , SelectField , DateField
from wtforms.validators  import DataRequired , email , EqualTo , ValidationError
from .models import Admin
from flask_login import current_user

class AdminRegForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired()])
    password_hash = PasswordField('Password' , validators = [DataRequired()])
    confirm_pwd= PasswordField('Confirm Password' , validators = [DataRequired() , EqualTo('password_hash')])
    email = StringField('email' , validators = [DataRequired()])
    submit = SubmitField('SignUp')


    def validate_username(self , username):
        admin=Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('That username is already taken.Please choose a different one')
    def validate_confirm_pwd(self , confirm_pwd):
        admin=Admin.query.filter_by(confirm_pwd=confirm_pwd.data).first()
        if admin:
            raise ValidationError()
    def validate_email(self , email):
        admin=Admin.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('That email is already taken.Please choose a different one') 

class AdminLoginForm(FlaskForm):
    email = StringField('emailAddress' , validators = [DataRequired()])
    password_hash = PasswordField('Password' , validators = [DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired()])
    email = StringField('Email' , validators = [DataRequired()])
    submit = SubmitField('Update')

    def validate_username(self , username):
        if username.data != current_user.username:
            user = Admin.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is already taken.Please choose a different one')

   
    def validate_email(self , email):
        if email.data != current_user.email:
            user = Admin.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken.Please choose a different one')