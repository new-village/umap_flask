from flask import Blueprint, request, redirect, url_for, abort, render_template
from flask_login import login_user, logout_user
from flask_pymongo import ObjectId
from app import mongo, login_manager
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        # Valid User/Password
        user = User.search(request.form["email"].lower())
        if user and user.valid_password(request.form["password"]):
            login_user(user)
            return redirect(request.args.get("next") or url_for("index.main"))
        else:
            return abort(401)
    else:
        # If a user is not exist, render create user page
        if mongo.db.users.count() == 0:
            mode = "/create/"
        else:
            mode = "/login/"
        return render_template("login.html", mode=mode)


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index.main"))


@auth.route('/create/', methods=["POST"])
def create():
    user = User(request.form["email"], request.form["password"])
    if user.save():
        login_user(user)
        return redirect(request.args.get("next") or url_for("index.main"))
    else:
        return abort(401)


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({"_id": user_id})
    return User(u["_id"], u["password"])


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
