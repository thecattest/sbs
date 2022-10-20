from flask import Blueprint, jsonify, make_response, abort, redirect, request
from db_init import *
from flask_login import current_user

api_blueprint = Blueprint('api', __name__)


def check_user_is_authenticated(decorating_func):
    def decorated_func(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(make_response(jsonify({'error': 'not authenticated'}), 403))
        decorating_func(*args, **kwargs)
    return decorated_func


@api_blueprint.route('/api/something/<int:some_id>', methods=['GET'])
@check_user_is_authenticated
def get_something(some_id):
    db = db_session.create_session()
    # do something
    response = {
        'some': 'thing',
        'id': some_id
    }
    db.close()
    return make_response(jsonify(response), 200)
