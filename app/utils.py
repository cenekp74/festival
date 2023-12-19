from .routs import db, Film, Beseda, Workshop
from . import ALLOWED_EXTENSIONS

def get_rooms():
    rooms = set()
    rooms.update([r[0] for r in list(db.session.query(Film.room).distinct().all())])
    rooms.update([r[0] for r in list(db.session.query(Beseda.room).distinct().all())])
    rooms.update([r[0] for r in list(db.session.query(Workshop.room).distinct().all())])
    return list(rooms)

def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions