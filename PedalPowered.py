# TO RUN, COMMAND IS python -m flask --app Test run
from flask import Flask, render_template, url_for
app = Flask(__name__)

#Protects against messing with logins 
app.config['SECRET KEY'] = '4y53qC839KwtRk0fXDdnJs5N7TYaDocIsD7S6MCN'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logride")
def logride():
    return render_template("logride.html", title="Log a Ride")

@app.route("/stats")
def stats():
    return render_template("stats.html", title="Your Stats")