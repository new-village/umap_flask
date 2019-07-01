from flask import Blueprint

app = Blueprint('action', __name__)


@app.route("/action")
def hello():
    return "This is the action.py"
