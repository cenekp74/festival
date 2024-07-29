from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'dev'
app.config.from_pyfile('../instance/config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['ALBUMS_JSON'] = 'app/static/fotogalerie/albums.json'
app.config['VALID_ROOMS'] = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', '1.A', '2.A', '3.A', '2.B', '3.B', 'IVT1', 'IVT2', 'MU', 'Bi', 'Fy', 'Ch', 'Chl']
app.config['WIP_MODE'] = True # work in progress mode - pokud neni user prihlasen tak odkaze z programu, hostu a workshopu na /wip

UPLOAD_FOLDER = 'app/static/upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from .utils import update_rooms, load_albums
try: # tohle je v try: except, protoze kdyz se spousti stranka poprvy (a neni vytvorena databaze), tak to failne
    update_rooms()
except Exception as e:
    print(f'Failed to load rooms from db: {e}')
load_albums()

from .api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api')

from .fotogalerie import fotogalerie as fotogalerie_blueprint
app.register_blueprint(fotogalerie_blueprint, url_prefix='/fotogalerie')

from .edit_program import edit_program as edit_program_blueprint
app.register_blueprint(edit_program_blueprint)

from app import routs