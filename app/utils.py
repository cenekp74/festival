from .routs import db, Film, Beseda, Workshop
from . import ALLOWED_EXTENSIONS

def get_rooms() -> dict:
    rooms = dict()
    for day in [1, 2, 3]:
        rooms[day] = set()
        rooms[day].update([r[0] for r in list(db.session.query(Film.room).filter(Film.day == day).distinct().all())])
        rooms[day].update([r[0] for r in list(db.session.query(Beseda.room).filter(Beseda.day == day).distinct().all())])
        rooms[day].update([r[0] for r in list(db.session.query(Workshop.room).filter(Workshop.day == day).distinct().all())])
    return rooms

def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def correct_uid(uid, h_allowed=True):
    if '_' not in uid: return False
    if len(uid.split('_')) != 2: return False
    item_type, item_id = uid.split('_')
    if not item_id.isdigit(): return False
    if h_allowed:
        if item_type not in ['w', 'b', 'f', 'h']: return False
    else:
        if item_type not in ['w', 'b', 'f']: return False
    return True