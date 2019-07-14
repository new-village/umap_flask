from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo


def launch_app():
    # Load Flask Application
    app = Flask(__name__)
    app.config.from_pyfile("../.env")

    # app.config["SECRET_KEY"] = "secret"
    # app.config["MONGO_URI"] = "mongodb://localhost:27017/umap"

    # Load Mongo DB
    login_manager.init_app(app)
    mongo.init_app(app)

    # Load Views
    from views import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app


login_manager = LoginManager()
mongo = PyMongo()
app = launch_app()

if __name__ == "__main__":
    app.run()
