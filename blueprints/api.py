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
        return decorating_func(*args, **kwargs)

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


@api_blueprint.route('/api/exams/<int:year_n>/<int:month_n>', methods=['GET'])
def get_exams_by_month(year_n, month_n):
    if month_n not in range(0, 12):
        return make_response(jsonify({'error': 'month does not exist'}), 400)

    response = dict()
    session = db_session.create_session()
    start_time, end_time = get_first_and_last_month_day(year_n, month_n)
    exams = session.query(Exam).filter(Exam.date >= start_time, Exam.date <= end_time).all()
    exams_resp = dict()
    for i in exams:
        exam: Exam = i
        exam_day = exam.date.day
        resp = dict()
        resp['id'] = exam.id
        resp['title'] = exam.type.title
        subjects = {}
        for sub in exam.get_subjects():
            subjects[sub] = session.query(Subject).filter(Subject.id==sub).first().title
        resp['subjects'] = subjects
        if exam_day in exams_resp:
            exams_resp[exam_day].append(resp)
        else:
            exams_resp[exam_day] = [resp]
        response['exams'] = exams_resp
        response['user_role'] = current_user.role
        return make_response(response, 200)

