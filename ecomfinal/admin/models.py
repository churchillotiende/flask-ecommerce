from ecomfinal import db
from flask_login import UserMixin
from ecomfinal import login_manager
from sqlalchemy.orm import declarative_base

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
class Admin(UserMixin , db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(30) , nullable = False , unique = True)
    password_hash = db.Column(db.String(130) , nullable = False)
    username = db.Column(db.String(30) , nullable = False , unique = True)
    email = db.Column(db.String(30) , nullable = False , unique = True)
    password_hash = db.Column(db.String(130) , nullable = False)
    confirm_pwd = db.Column(db.String(130) , nullable = False)
    image_file = db.Column(db.String(128) , nullable = False , default = 'default.jpg')

db.create_all()