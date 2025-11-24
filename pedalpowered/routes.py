from flask import render_template, url_for, flash, redirect
from pedalpowered.models import User, rides
from pedalpowered.forms import RegisterForm, LoginForm
from pedalpowered import app, db, bcrypt
from flask_login import login_user

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
        #Hash the password so it can't be taken directly off the database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created, please log in.','success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form = form)

@app.route("/", methods = ['GET','POST'])
@app.route("/login", methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'Welcome back {form.username.data}!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login failed, please try again.','danger')
    return render_template("login.html", title="Login", form=form)

#python -m flask --app PedalPowered run