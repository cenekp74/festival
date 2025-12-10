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
    perm_program_edit = db.Column(db.Integer, nullable=False, default=0)
    perm_shop = db.Column(db.Integer, nullable=False, default=0)
    perm_fotogalerie = db.Column(db.Integer, nullable=False, default=0)

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    besedy = db.relationship('Beseda', backref='host')
    picture_filename = db.Column(db.String(20), nullable=False, default='default.png')

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100))
    language = db.Column(db.String(10))
    short_description = db.Column(db.String(100))
    description = db.Column(db.String(1800))
    picture_filename = db.Column(db.String(20), nullable=False, default='default.png')
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))
    reflexe_link = db.Column(db.String(200))
    filename = db.Column(db.String(50))
    vg = db.Column(db.Integer, default=0, nullable=False) # je jen pro vyssi gymnazium?
    hidden = db.Column(db.Integer, default=0, nullable=False) # mel by byt film skryty na strance filmy (zobrazovat se jen v programu)?

    @property
    def serialize(self):
       return {
           "id": self.id,
           "item_type": "film",
           "uid": 'f_' + str(self.id),
           "name": self.name,
           "link": self.link if self.link else "",
           "language": self.language if self.language else "",
           "short_description": self.short_description if self.short_description else "",
           "time_from": self.time_from,
           "time_to": self.time_to,
           "day": self.day,
           "room": self.room,
           "reflexe_link": self.reflexe_link if self.reflexe_link else "",
           "filename": self.filename if self.filename else "",
           "vg": self.vg,
       }

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))
    description = db.Column(db.String(1000))
    picture_filename = db.Column(db.String(20), nullable=False, default='default.png')
    vg = db.Column(db.Integer, default=0, nullable=False) # je jen pro vyssi gymnazium?

    @property
    def serialize(self):
       return {
           "id": self.id,
           "item_type": "workshop",
           "uid": 'w_' + str(self.id),
           "name": self.name,
           "time_from": self.time_from,
           "time_to": self.time_to,
           "day": self.day,
           "room": self.room,
           "description": self.description,
           "picture_filename": self.picture_filename
       }

class Beseda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    time_from = db.Column(db.String(5))
    time_to = db.Column(db.String(5))
    day = db.Column(db.Integer)
    room = db.Column(db.String(10))
    vg = db.Column(db.Integer, default=0, nullable=False) # je jen pro vyssi gymnazium?

    @property
    def serialize(self):
       host = Host.query.get(self.host_id)
       host_name = None
       if host:
           host_name = host.name
       return {
           "id": self.id,
           "item_type": "beseda",
           "uid": 'b_' + str(self.id),
           "name": self.name,
           "time_from": self.time_from,
           "time_to": self.time_to,
           "day": self.day,
           "room": self.room,
           "host_id": self.host_id,
           "host": host_name
       }
    
class ShopItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    item_type = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
       return {
           "id": self.id,
           "name": self.name,
           "item_type": self.item_type,
           "price": self.price
       }