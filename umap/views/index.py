from flask import Blueprint, Response, render_template
from flask_login import login_required, UserMixin
from flask_pymongo import PyMongo
from .common import mongo

app = Blueprint('index', __name__)


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.email = name
        self.password = password


# ログイン用ユーザー作成
users = {
    1: User(1, "sample@gmail.com", "password"),
    2: User(2, "test@gmail.com", "password")
}


@app.route("/")
@app.route("/index")
@login_required
def index():
    key = {"email": "sample@gmail.com"}
    user = {"email": "sample@gmail.com", "password": "password"}
    result = mongo.db.users.update(key, user, upsert=True)
    online_users = [d for d in mongo.db.users.find()]
    return render_template("index.html", online_users=online_users)
