from .routs import db, Film, Beseda, Workshop

def get_rooms():
    rooms = set()
    rooms.update([r[0] for r in list(db.session.query(Film.room).distinct().all())])
    rooms.update([r[0] for r in list(db.session.query(Beseda.room).distinct().all())])
    rooms.update([r[0] for r in list(db.session.query(Workshop.room).distinct().all())])
    
    return list(rooms)