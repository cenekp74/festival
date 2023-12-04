import json

def load_db():
    return json.load(open('app/static/db.json', 'r'))

def commit_db(db):
    if "films" not in db or "workshops" not in db or "hoste" not in db:
        raise Exception('invalid db provided')
        return
    json.dump(db, open('app/static/db.json', 'w'))

def get_new_film_id(db=None):
    if db == None:
        db = load_db()
    return db["films"][-1]["id"] + 1