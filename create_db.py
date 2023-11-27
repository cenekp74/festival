from app import db 
from app.dbClasses import User
from app import app

with app.app_context():
    db.create_all()