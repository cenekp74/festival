from flask import Blueprint, jsonify
from app.db_classes import Host, User, Film, Beseda, Workshop
from app import db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/query/film/all')
def query_film_all():
    return jsonify([item.serialize for item in Film.query.all()])

@api_blueprint.route('/query/program_items/all')
def query_all_program_items():
    result = []
    result += [item.serialize for item in Film.query.all()]
    result += [item.serialize for item in Beseda.query.all()]
    result += [item.serialize for item in Workshop.query.all()]
    return jsonify(result)