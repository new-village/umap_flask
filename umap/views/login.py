from flask import Blueprint, request, Response, abort, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, UserMixin
from collections import defaultdict


app = Blueprint('login', __name__)


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password


# ログイン用ユーザー作成
users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}

# ユーザーチェックに使用する辞書作成


def nested_dict(): return defaultdict(nested_dict)


user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id


@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # ユーザーチェック
        if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["username"]]["id"]))
            return redirect(request.args.get("next") or url_for("index.index"))
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return Response('''
    logout success!<br />
    <a href="/login/">LOGIN</a><br />
    <a href="/index">RESTRICTED AREA</a><br />
    <a href="/action">NON-RESTRICTED AREA</a><br />
    ''')
