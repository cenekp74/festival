from flask import Blueprint, jsonify, request
from app.db_classes import Film, Beseda, Workshop
from app.utils import get_all_rooms

api = Blueprint('api', __name__)

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
