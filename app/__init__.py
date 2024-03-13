from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '5e72ba27fc6a863eed13c27e6750bd25ab0be9ff55ac0e34823d966c1ce4896026992f2639857117'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['ALBUMS_JSON'] = 'app/static/fotogalerie/albums.json'

UPLOAD_FOLDER = 'app/static/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from .utils import update_rooms, load_albums
update_rooms()
load_albums()

from .api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

from .fotogalerie import fotogalerie as fotogalerie_blueprint
app.register_blueprint(fotogalerie_blueprint, url_prefix='/fotogalerie')

from app import routs