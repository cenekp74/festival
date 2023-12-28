from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    short_description = db.Column(db.String(100))
    besedy = db.relationship('Beseda', backref='host')
    picture_filename = db.Column(db.String(20), nullable=False, default='default.png')

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100))
    language = db.Column(db.String(10))
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))
    author = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    picture_filename = db.Column(db.String(20), nullable=False, default='default.png')

class Beseda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))