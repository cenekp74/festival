import json

def load_db():
    return json.load(open('app/static/db.json', 'r'))