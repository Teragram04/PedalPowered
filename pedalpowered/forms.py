from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from pedalpowered.models import User
from flask_login import current_user
from datetime import date, timedelta

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


class UpdateAcctForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(),Length(min=2,
    max= 20, message="Username must be between 5-20 characters long")])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit_registration = SubmitField('Submit Changes')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username taken, try again')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('This email has an associated account already')
            

class NewRideForm(FlaskForm):
    title = StringField('*Ride Title', validators=[DataRequired()])
    distance = FloatField('*Distance in Miles: (00.00)',validators=[DataRequired()])
    ride_date = DateField('Date', validators=[DataRequired()], format= '%Y-%m-%d')
    gas_price = FloatField('Avg Gas Cost (0.00)')
    car_mpg = FloatField('Avg Car MPG (00.0)')
    comment = StringField('Notes')
    submit_registration = SubmitField('Submit my Ride!')

class FilterByDateForm(FlaskForm):
    start_date = DateField('Start Date', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Filter')