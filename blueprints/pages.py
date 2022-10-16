from flask import Blueprint, jsonify, make_response, abort, redirect, request
from db_init import *
from flask_login import login_user, login_required, logout_user, current_user
from utils import send_html

pages_blueprint = Blueprint('pages', __name__)


@pages_blueprint.route('/')
def page_index():
    return send_html('index.html')

@pages_blueprint.route('/login')
def page_login():
    return send_html('login.html')


@pages_blueprint.route('/logout')
@login_required
def page_logout():
    logout_user()
