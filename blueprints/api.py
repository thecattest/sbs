from flask import Blueprint, jsonify, make_response, abort, redirect, request, session
from db_init import *
from flask_login import current_user, login_user, login_required
import re
from .methods import *
from .settings import *
from datetime import datetime
from datetime import timedelta

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
    print(current_user)
    db = db_session.create_session()
    response = {
        'some': 'thing',
        'id': some_id
    }
    db.close()
    return make_response(jsonify(response), 200)


@api_blueprint.route('/api/code/', methods=['POST'])
def generate_auth_code():
    r = request.json
    if 'phone' not in r:
        return make_response(jsonify({'error': 'missing argument'}), 400)

    phone = r['phone']
    if not check_phone_number(phone):
        make_response(jsonify({'error': 'invalid number'}), 400)

    phone_f = format_phone_number(phone)
    session = db_session.create_session()
    exist_user: User = session.query(User).filter(User.phone == phone_f).first()

    if exist_user is None:
        return make_response(jsonify({'error': 'user does not exist'}), 404)

    code = generate_sms_code()
    exist_user.sms_code = code
    exist_user.sms_code_valid_thru = datetime.utcnow() + timedelta(seconds=SMS_CODE_TIMEOUT)
    session.commit()
    session.close()
    return make_response(jsonify({'ok': 'true'}), 204)


@api_blueprint.route('/api/login/', methods=['POST'])
def make_login():
    r = request.json

    if 'phone' not in r or 'code' not in r:
        return make_response(jsonify({'error': 'missing argument'}), 400)

    phone = r['phone']
    if not check_phone_number(phone):
        make_response(jsonify({'error': 'invalid number'}), 400)

    phone_f = format_phone_number(phone)

    session = db_session.create_session()
    exist_user: User = session.query(User).filter(User.phone == phone_f).first()

    if exist_user is None:
        return make_response(jsonify({'error': 'user does not exist'}), 404)

    code = r['code']
    if not check_sms_code(exist_user.sms_code, exist_user.sms_code_valid_thru, code):
        return make_response(jsonify({'error': 'wrong code'}), 403)

    exist_user.sms_code = None
    exist_user.sms_code_valid_thru = None
    session.commit()
    login_user(exist_user, True)
    session.close()
    return make_response(jsonify({'ok': 'true'}), 204)
