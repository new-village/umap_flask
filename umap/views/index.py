from flask import current_app, Blueprint, render_template
from flask_login import login_required
from app import mongo, login_manager
from models import User


index = Blueprint('index', __name__)


@index.route("/")
@index.route("/index")
@login_required
def main():
    key = {"email": "sample@gmail.com"}
    # user = {"email": "sample@gmail.com", "password": "password"}
    # result = mongo.db.users.update(key, user, upsert=True)
    user_info = User.search("kazuki.niimura@gmail.com")
    return render_template("index.html", user=user_info)


@index.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("images/favicon.ico")
