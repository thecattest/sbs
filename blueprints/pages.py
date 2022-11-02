from flask import Blueprint, redirect, send_file, send_from_directory
from flask_login import login_required, logout_user


FRONTEND = 'frontend'
pages_blueprint = Blueprint('pages', __name__, template_folder=FRONTEND)


@pages_blueprint.route(f'/{FRONTEND}/<path:path>')
def send_static(path):
    return send_from_directory(FRONTEND, path)


@pages_blueprint.route('/')
def page_index():
    return redirect('/calendar')


@pages_blueprint.route('/calendar')
def calendar():
    return send_from_directory(FRONTEND, 'calendar.html')




@pages_blueprint.route('/login')
def page_login():
    return send_from_directory(FRONTEND, 'login.html')


@pages_blueprint.route('/logout')
@login_required
def page_logout():
    logout_user()
