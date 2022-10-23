from flask import Blueprint, jsonify, make_response, abort, redirect, request
from db_init import *
from flask_login import current_user
import re
from .methods import *
from .settings import *
from datetime import datetime
from datetime import timedelta

NUM_RE = re.compile(r'((\+7|7|8)+([0-9]){10})$')
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
    return make_response(204)
