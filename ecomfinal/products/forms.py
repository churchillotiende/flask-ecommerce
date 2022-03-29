from wtforms import StringField , SubmitField , PasswordField , BooleanField , IntegerField , TextAreaField , SelectField , DateField
from wtforms.validators  import DataRequired , email , EqualTo , ValidationError
from flask_wtf.file import FileAllowed , FileField , FileRequired
from flask_wtf import FlaskForm

class AddProducts(FlaskForm):
    name = StringField('name' , validators = [DataRequired()])
    price = StringField('Price' , validators = [DataRequired()])
    discount= StringField('Discount' ,default = 0)
    stock = StringField('Stock' , validators = [DataRequired()])
    description = TextAreaField('Description' , validators = [DataRequired()])
    color  =StringField('Colors' , validators = [DataRequired()])
    image_1 = FileField('Image 1' , validators = [FileAllowed(['jpg' , 'png' , 'jpeg' , 'gif'])])
    image_2 = FileField('Image 2' , validators = [FileAllowed(['jpg' , 'png' , 'jpeg' , 'gif'])])
    image_3 = FileField('Image 3' , validators = [FileAllowed(['jpg' , 'png' , 'jpeg' , 'gif'])])
    submit = SubmitField('Add Product')

