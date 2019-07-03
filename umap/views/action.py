from flask import Blueprint, render_template

app = Blueprint('action', __name__)


@app.route("/action")
def hello():
    return render_template("action.html")
