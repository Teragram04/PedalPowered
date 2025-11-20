from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Used to write classes in py that are THEN converted to html within the template

class Register(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=5,
    max= 20, message="Username must be between 5-20 characters long")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit_registration = SubmitField('Register!')

class Login(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=5,
    max= 20)])

    #email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

    remember = BooleanField('Remember Login')

    submit_registration = SubmitField('Login!')