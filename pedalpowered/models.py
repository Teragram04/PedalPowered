from pedalpowered import db, login_manager
from datetime import datetime
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
    ride_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    distance = db.Column(db.Float, nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"rides('{self.ride_date}',{self.distance})"
    