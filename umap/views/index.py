from flask import current_app, Blueprint, render_template
from flask_login import login_required
from app import mongo, login_manager


index = Blueprint('index', __name__)


@index.route("/")
@index.route("/index")
@login_required
def main():
    key = {"email": "sample@gmail.com"}
    user = {"email": "sample@gmail.com", "password": "password"}
    result = mongo.db.users.update(key, user, upsert=True)
    return render_template("index.html", user=mongo.db.users.find_one(key))


@index.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("images/favicon.ico")
