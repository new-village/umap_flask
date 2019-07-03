from flask import Blueprint, Response, render_template
from flask_login import login_required, UserMixin
from flask_pymongo import PyMongo
from .base import mongo

app = Blueprint('index', __name__)


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password


users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}


@app.route("/")
@app.route("/index")
@login_required
def index():
    online_users = list(mongo.db.users.find())
    return render_template("index.html", online_users=online_users)
