from enum import unique
from ecomfinal import db
from flask_login import UserMixin
from ecomfinal import login_manager
from datetime import datetime
from sqlalchemy.orm import declarative_base
import json

@login_manager.user_loader
def user_loader(user_id):
    return CustomerRegister.query.get(user_id)

class CustomerRegister(UserMixin , db.Model):
    __tablename__ = 'customerregister'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(30) ,nullable = False , unique = True)
    city = db.Column(db.String(30) , nullable = False)
    country = db.Column(db.String(30) ,nullable = False)
    zip_code =db.Column(db.String(30) , nullable = False)
    address = db.Column(db.String(30) , nullable = False)
    email = db.Column(db.String(130) , nullable = False)
    date_created = db.Column(db.DateTime , default = datetime.utcnow)
    password = db.Column(db.String(130) , nullable = False)
    confirm = db.Column(db.String(130) , nullable = False)
    profile = db.Column(db.String(130) , unique = False , nullable = True, default = 'default.jpg')


class JsonEncodedDict(db.TypeDecorator):
	impl = db.Text
	def process_bind_param(self , value , dialect):
		if value is None:
			return '{}'
		else:
			return json.dumps(value)
	def process_result_value(self , value , dialect):
		if value is None:
			return {}
		else:
			return json.loads(value)

class CustomerOrder(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	invoice = db.Column(db.String(20) , unique = True , nullable = False)
	status = db.Column(db.String(20) , default = 'Pending' , nullable = False)
	customer_id = db.Column(db.Integer , unique = False , nullable = False)
	date_created = db.Column(db.DateTime , default = datetime.utcnow , nullable = False)
	orders = db.Column(JsonEncodedDict)


db.create_all()