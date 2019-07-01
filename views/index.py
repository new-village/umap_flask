from flask import Blueprint

app = Blueprint('index', __name__)


@app.route("/")
@app.route("/index")
def hello():
    return "Hello from index.py"
