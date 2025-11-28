from pedalpowered import db, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
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
    ride_date = db.Column(db.DateTime, nullable = False)
    #If you want time automatically added, use default = lambda: datetime.now(timezone.utc)
    title = db.Column(db.String, nullable = False)
    distance = db.Column(db.Float, nullable = False)
    gas_price = db.Column(db.Float, nullable = True)
    car_mpg = db.Column(db.Float, nullable = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    gas_money_saved = db.Column(db.Float, nullable = True)
    user_comment = db.Column(db.String, nullable = False)

    #Can't do math within an SQLITE column, so define a function and then assign the value to the model
    def calculate_money_saved(self):
        if self.distance and self.car_mpg and self.gas_price and self.car_mpg != 0:
            self.gas_money_saved = round(((self.distance / self.car_mpg) * self.gas_price),2)
        else:
            self.gas_money_saved = 0
        

    def __repr__(self):
        return f"rides('{self.ride_date}',{self.distance})"
    