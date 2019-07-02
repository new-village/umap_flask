from flask import Blueprint, Response
from flask_login import login_required, UserMixin

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
def hello():
    return Response('''
            RESTRICTED AREA: Hello from index.py<br />
            <a href="/action">NON-RESTRICTED AREA</a><br />
            <a href="/logout/">LOGOUT</a><br />
            ''')
