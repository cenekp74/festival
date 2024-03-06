from flask import Blueprint, jsonify
from app.db_classes import Host, User, Film, Beseda, Workshop
from app import db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query/film/all')
def query_film_all():
    return jsonify([item.serialize for item in Film.query.all()])

@api_blueprint.route('/query/film/day')
def query_film_by_dat_all():
    result = []
    for day in [1, 2, 3]:
        result.append([item.serialize for item in Film.query.filter_by(day=day)])
    return jsonify(result)

@api_blueprint.route('/query/program_items/all')
def query_all_program_items():
    result = []
    result += [item.serialize for item in Film.query.all()]
    result += [item.serialize for item in Beseda.query.all()]
    result += [item.serialize for item in Workshop.query.all()]
    return jsonify(result)

@api_blueprint.route('/query/program_items/day=<day>')
def query_program_items_by_day(day):
    result = []
    result += [item.serialize for item in Film.query.filter_by(day=day)]
    result += [item.serialize for item in Beseda.query.filter_by(day=day)]
    result += [item.serialize for item in Workshop.query.filter_by(day=day)]
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