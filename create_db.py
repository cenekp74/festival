from app import db 
from app.db_classes import User, Film, Workshop, Beseda, Host
from app import app

with app.app_context():
    db.create_all()