from flask import Blueprint, jsonify, request, abort
from app.db_classes import Film, Beseda, Workshop
from app.utils import get_all_rooms, correct_uid, update_rooms
from flask_login import login_required
from .decorators import admin_required
from . import db

api = Blueprint('api', __name__)

@api.route('/update_from_json', methods=['POST'])
@login_required
@admin_required
def update_from_json(): # updatuje program z json ve formatu {"uid":{"time_from":time, "time_to":time, "room":room}} (funkce pro interaktivni editovani programu)
    content = request.json
    for uid, item_details in content.items():
        if not correct_uid(uid, h_allowed=False): abort(400)
        item_type, item_id = uid.split('_')
        item_id = int(item_id)
        match item_type:
            case 'f': item = Film.query.get(item_id)
            case 'b': item = Beseda.query.get(item_id)
            case 'w': item = Workshop.query.get(item_id)
        item.time_from = item_details['time_from']
        item.time_to = item_details['time_to']
        item.room = item_details['room']
        db.session.commit()
        update_rooms()
    return '200'

@api.route('/query/film')
def query_film():
    args = request.args.to_dict()
    return jsonify([item.serialize for item in Film.query.filter_by(**args)])

@api.route('/query/film/day')
def query_film_by_day():
    result = []
    for day in [1, 2, 3]:
        result.append([item.serialize for item in Film.query.filter_by(day=day)])
    return jsonify(result)

@api.route('/query/program_items')
def query_program_items():
    args = request.args.to_dict()
    result = []
    result += [item.serialize for item in Film.query.filter_by(**args)]
    result += [item.serialize for item in Beseda.query.filter_by(**args)]
    result += [item.serialize for item in Workshop.query.filter_by(**args)]
    return jsonify(result)

@api.route('/query/program_items/day')
def query_program_items_by_day_all():
    result = []
    for day in [1, 2, 3]:
        result.append([])
        result[day-1] += [item.serialize for item in Film.query.filter_by(day=day)]
        result[day-1] += [item.serialize for item in Beseda.query.filter_by(day=day)]
        result[day-1] += [item.serialize for item in Workshop.query.filter_by(day=day)]
    return jsonify(result)

@api.route('/get_rooms')
def rooms():
    return jsonify(get_all_rooms())

@api.route('/get_rooms_for_films') #jenom mistnosti s filmama
def film_rooms():
    return jsonify(get_all_rooms(films_only=True))
