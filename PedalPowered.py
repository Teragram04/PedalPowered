# TO RUN, COMMAND IS python -m flask --app Test run
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/logride")
def logride():
    return render_template("logride.html")