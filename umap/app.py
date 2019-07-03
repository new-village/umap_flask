from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required

from collections import defaultdict
from views import index, action, login
from views.base import mongo

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo.init_app(app)

app.register_blueprint(index.app)
app.register_blueprint(action.app)
app.register_blueprint(login.app)


class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password


users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password")
}


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route("/sample")
@login_required
def hello():
    return "Hello from index.py"


if __name__ == "__main__":
    app.run()
