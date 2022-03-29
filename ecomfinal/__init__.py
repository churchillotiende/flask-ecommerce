from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import IMAGES ,UploadSet, configure_uploads
from flask_msearch import Search
import os
import pymysql
pymysql.install_as_MySQLdb()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '27582879540f14b4bace0d2a86870526'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:11055@localhost/candle_glows'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
photos = UploadSet('photos' , IMAGES)
configure_uploads(app ,photos)
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)
search = Search()
search.init_app(app)
login_manager = LoginManager(app)

from ecomfinal.admin import routes
from ecomfinal.products import routes
from ecomfinal.carts import carts
from ecomfinal.customers import routes


