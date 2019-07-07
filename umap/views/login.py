from flask import Blueprint, request, Response, abort, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, UserMixin
from collections import defaultdict


app = Blueprint('login', __name__)


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

# ユーザーチェックに使用する辞書作成


def nested_dict(): return defaultdict(nested_dict)


user_check = nested_dict()
for i in users.values():
    user_check[i.email]["password"] = i.password
    user_check[i.email]["id"] = i.id


@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # ユーザーチェック
        if(request.form["email"] in user_check and request.form["password"] == user_check[request.form["email"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["email"]]["id"]))
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
