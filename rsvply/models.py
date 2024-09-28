from datetime import datetime
from rsvply import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}, {self.username}', '{self.email}')"
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    expiry = db.Column(db.DateTime(timezone=True), nullable=False)
    description =  db.Column(db.Text, nullable=False)
    location = db.Column(db.String(30), nullable=False)
    hash = db.Column(db.String(64), unique=True, nullable=False)

class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    attending = db.Column(db.Boolean(), nullable=False, default=False)
    checked_in = db.Column(db.Boolean(), nullable=False, default=False)


    event_id = db.Column(db.Integer, nullable=False)
    hash = db.Column(db.String(64), unique=True, nullable=False) # will be updated when hit submit



    def __repr__(self):
        return f"Event('{self.name}', '{self.email}', '{self.event_id}')"
    
