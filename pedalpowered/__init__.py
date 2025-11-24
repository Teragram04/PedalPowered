from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
#Protects against messing with logins 
app.config['SECRET_KEY'] = '4y53qC839KwtRk0fXDdnJs5N7TYaDocIsD7S6MCN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#Represent database structures with classes (models). Each class is its own table in the database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


csrf = CSRFProtect(app)

from pedalpowered import routes
