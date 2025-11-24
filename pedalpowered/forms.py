from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from pedalpowered.models import User

#Used to write classes in py that are THEN converted to html within the template

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=2,
    max= 20, message="Username must be between 5-20 characters long")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])

    submit_registration = SubmitField('Register!')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username taken, try again')
        
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('This email has an associated account already')




class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=2,
    max= 20)])

    #email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])

    remember = BooleanField('Remember Login')

    submit_registration = SubmitField('Login!')