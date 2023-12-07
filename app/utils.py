from .routs import db, Film

def get_rooms():
    rooms = set()
    rooms.update([r[0] for r in list(db.session.query(Film.room).distinct().all())])
    return list(rooms)