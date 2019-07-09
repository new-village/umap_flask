from flask import Blueprint, request, Response, abort, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, UserMixin
from collections import defaultdict
from models import User
from .common import mongo


app = Blueprint('login', __name__)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # Valid User/Password
        u = mongo.db.users.find_one({"email": request.form["email"]})
        if u and u["password"] == request.form["password"]:
            user = User(u["_id"], u["email"], u["password"])
            login_user(user)
            return redirect(request.args.get("next") or url_for("index.index"))
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for("index.index"))
