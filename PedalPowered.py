# TO RUN, COMMAND IS python -m flask --app Test run
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
from flask_wtf.csrf import CSRFProtect
app = Flask(__name__)
#Protects against messing with logins 
app.config['SECRET_KEY'] = '4y53qC839KwtRk0fXDdnJs5N7TYaDocIsD7S6MCN'
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
        flash(f'Welcome {form.username.data}!','success')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form = form)

@app.route("/")
@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)