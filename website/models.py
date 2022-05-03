from pytz import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100000))
    data_amt = db.Column(db.Integer())
    label = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    in_take=db.Column(db.Integer)
    


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    notes = db.relationship('Note')
    max_spend=db.Column(db.Integer())

# print(User.query.order_by(User.email).all())
#s = User.query.filter(User.email.endswith('@gmail.com')).all()
# print(s[2].password)
