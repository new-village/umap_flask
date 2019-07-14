from flask import Blueprint, request, redirect, url_for, abort, render_template
from flask_login import login_user, logout_user
from flask_pymongo import ObjectId
from app import mongo, login_manager
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # Valid User/Password
        u = mongo.db.users.find_one({"email": request.form["email"]})
        if u and u["password"] == request.form["password"]:
            user = User(u["_id"], u["email"], u["password"])
            login_user(user)
            return redirect(request.args.get("next") or url_for("index.main"))
        else:
            return abort(401)
    else:
        return render_template("login.html")


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index.main"))


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(u["_id"], u["email"], u["password"])


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
