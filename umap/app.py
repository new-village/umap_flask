from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required
from flask_pymongo import PyMongo, ObjectId
from collections import defaultdict
from views import index, login
from views.common import mongo
from models import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"
app.config["MONGO_URI"] = "mongodb://localhost:27017/umap"
mongo.init_app(app)

app.register_blueprint(index.app)
app.register_blueprint(login.app)


@login_manager.user_loader
def load_user(user_id):
    u = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(u["_id"], u["email"], u["password"])


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("images/favicon.ico")


if __name__ == "__main__":
    app.run()
