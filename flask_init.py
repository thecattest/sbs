from flask import Flask, redirect
from flask_login import LoginManager

from db_init import *
from blueprints import api_blueprint, pages_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahsdfkjiurwpjcnspwwqiuqnc'
app.register_blueprint(api_blueprint)
app.register_blueprint(pages_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.unauthorized_handler(callback=(lambda: redirect('/login')))


@login_manager.user_loader
def load_user(user_id):
    db = db_session.create_session()
    db.expire_on_commit = False
    return db.query(User).get(user_id)
