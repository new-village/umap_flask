from flask import Blueprint, Response, render_template
from flask_login import login_required, UserMixin
from flask_pymongo import PyMongo
from .common import mongo
from models import User

app = Blueprint('index', __name__)


@app.route("/")
@app.route("/index")
@login_required
def index():
    key = {"email": "sample@gmail.com"}
    user = {"email": "sample@gmail.com", "password": "password"}
    result = mongo.db.users.update(key, user, upsert=True)
    online_users = [d for d in mongo.db.users.find()]
    return render_template("index.html", online_users=online_users)
