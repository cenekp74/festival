from flask import Blueprint, jsonify, request
from app.db_classes import Host, User, Film, Beseda, Workshop
from app import db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query/film')
def query_film():
    args = request.args.to_dict()
    return jsonify([item.serialize for item in Film.query.filter_by()])

@api_blueprint.route('/query/film/day')
def query_film_by_day():
    result = []
    for day in [1, 2, 3]:
        result.append([item.serialize for item in Film.query.filter_by(day=day)])
    return jsonify(result)

@api_blueprint.route('/query/program_items')
def query_program_items():
    args = request.args.to_dict()
    result = []
    result += [item.serialize for item in Film.query.filter_by(**args)]
    result += [item.serialize for item in Beseda.query.filter_by(**args)]
    result += [item.serialize for item in Workshop.query.filter_by(**args)]
    return jsonify(result)

@api_blueprint.route('/query/program_items/day')
def query_program_items_by_day_all():
    result = []
    for day in [1, 2, 3]:
        result.append([])
        result[day-1] += [item.serialize for item in Film.query.filter_by(day=day)]
        result[day-1] += [item.serialize for item in Beseda.query.filter_by(day=day)]
        result[day-1] += [item.serialize for item in Workshop.query.filter_by(day=day)]
    return jsonify(result)