# TO RUN, COMMAND IS python -m flask --app Test run
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
from flask_wtf.csrf import CSRFProtect
import sqlite3
app = Flask(__name__)
#Protects against messing with logins 
app.config['SECRET_KEY'] = '4y53qC839KwtRk0fXDdnJs5N7TYaDocIsD7S6MCN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#Represent database structures with classes (models). Each class is its own table in the database
db = SQLAlchemy(app)

class User(db.Model):
    #Columns for table
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    password = db.Column(db.String(60), nullable=False)

    ridelog = db.relationship('rides', backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"

class rides(db.Model):
    #Columns for table
    id = db.Column(db.Integer, primary_key = True)
    ride_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    distance = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"rides('{self.ride_date}',{self.distance})"
    
    


csrf = CSRFProtect(app)



@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logride")
def logride():
    return render_template("logride.html", title="Log a Ride")

@app.route("/stats")
def stats():
    return render_template("stats.html", title="Your Stats")

@app.route("/register", methods = ['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Welcome to PedalPowered {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form = form)

@app.route("/", methods = ['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome back{form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("login.html", title="Login", form=form)

#python -m flask --app PedalPowered run