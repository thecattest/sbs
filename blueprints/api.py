from flask import Blueprint, jsonify, make_response, abort, redirect, request, session
from db_init import *
from flask_login import current_user, login_user, login_required
import re
from .methods import *
from .settings import *
from datetime import datetime
from datetime import timedelta

api_blueprint = Blueprint('api', __name__)


def check_user_is_authenticated():
    if not current_user.is_authenticated:
        abort(make_response(jsonify({'error': 'not authenticated'}), 403))


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
        resp['places'] = exam.places
        participants = session.query(Registration).filter(Registration.exam_id == exam.id).all()
        resp['participants'] = len(participants)
        resp['subject'] = exam.subject.title
        resp['date'] = exam.date
        if exam_day in exams_resp:
            exams_resp[exam_day].append(resp)
        else:
            exams_resp[exam_day] = [resp]
        response['exams'] = exams_resp
        if current_user.is_authenticated:
            response['user_role'] = current_user.role
            if current_user.role == User.ROLE_CLIENT:
                is_registered = session.query(Registration).filter(Registration.exam_id == exam.id,
                                                                   Registration.user_id == current_user.id).first()
                is_registered = False if is_registered is None else True
                response['registered'] = is_registered
        else:
            response['user_role'] = User.ROLE_CLIENT
        return make_response(response, 200)


@api_blueprint.route('/api/exam/<exam_id>', methods=['POST'])
def order_exam(exam_id):
    check_user_is_authenticated()

    if current_user.role == User.ROLE_ADMIN:
        return make_response(jsonify({'error': 'invalid role'}), 405)
    session = db_session.create_session()
    exam: Exam = session.query(Exam).filter(Exam.id == exam_id).first()
    if exam is None:
        return make_response(jsonify({'error': 'exam does not exist'}), 400)

    participants = session.query(Registration).all()
    if len(participants) >= exam.places:
        return make_response(jsonify({'error': 'places are over'}), 403)

    if (datetime.utcnow() - exam.date).days < 3:
        return make_response(jsonify({'error': 'registration are closed'}), 403)

    already_ordered = session.query(Registration).filter(Registration.exam_id == exam_id,
                                                         Registration.user_id == current_user.id).first()
    if already_ordered:
        return make_response(jsonify({'error': 'already ordered'}), 403)

    r = Registration()
    r.exam_id = exam.id
    r.user_id = current_user.id
    session.add(r)
    session.commit()
    resp = dict()
    resp['id'] = exam.id
    resp['title'] = exam.type.title
    resp['places'] = exam.places
    resp['participants'] = len(participants) + 1
    resp['subject'] = exam.subject.title
    resp['date'] = exam.date
    session.close()
    return make_response(jsonify({'exam': resp}), 200)


@api_blueprint.route('/api/exam/', methods=['POST'])
def create_exam():
    check_user_is_authenticated()

    if current_user.role == User.ROLE_CLIENT:
        return make_response(jsonify({'error': 'invalid role'}), 405)

    r = request.json
    if 'date' not in r or 'type' not in r or 'subject' not in r or 'places' not in r or 'price' not in r:
        return make_response(jsonify({'error': 'missing argument'}), 400)

    session = db_session.create_session()
    exam = Exam()
    exam.type_id = r['type']
    exam.places = r['places']
    exam.subject_id = r['subject']
    exam.price = r['price']
    exam.date = datetime.utcfromtimestamp(r['date'])
    session.add(exam)
    session.commit()

    resp = dict()
    resp['id'] = exam.id
    resp['title'] = exam.type.title
    resp['places'] = exam.places
    resp['participants'] = 0
    resp['subject'] = exam.subject.title
    resp['date'] = exam.date
    session.close()
    return make_response(jsonify({'exam': resp}), 200)


@api_blueprint.route('/api/my/', methods=['GET'])
def get_client_exams():
    check_user_is_authenticated()

    if current_user.role == User.ROLE_ADMIN:
        return make_response(jsonify({'error': 'invalid role'}), 405)

    session = db_session.create_session()
    user_exams = session.query(Registration).filter(Registration.user_id).all()

    response = {}
    exams = []
    for i in user_exams:
        reg: Registration = i
        exam = reg.exam
        resp = dict()
        resp['id'] = exam.id
        resp['type'] = exam.type_id
        resp['subject'] = exam.subject.title
        resp['date'] = exam.date
        exams.append(resp)
    response['exams'] = exams
    return make_response(jsonify(response), 200)


@api_blueprint.route('/api/exam/<exam_id>', methods=['GET'])
def get_exam_by_id(exam_id):
    check_user_is_authenticated()

    if current_user.role == User.ROLE_CLIENT:
        return make_response(jsonify({'error': 'invalid role'}), 501)

    session = db_session.create_session()
    exam: Exam = session.query(Exam).filter(Exam.id == exam_id).first()

    if exam is None:
        return make_response(jsonify({'error': 'exam does not exist'}), 404)

    response = dict()
    response['id'] = exam.id
    response['type'] = exam.type_id
    response['subject'] = exam.subject.title
    response['date'] = exam.date
    response['price'] = exam.price

    participants = session.query(Registration).filter(Registration.exam_id == exam_id).all()
    list_of_participants = []
    for i in participants:
        participant: Registration = i
        list_of_participants.append([participant.user.phone, participant.user.id])
    response['participants'] = list_of_participants
    return make_response(jsonify(response), 200)
