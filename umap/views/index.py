from flask import current_app, Blueprint, render_template
from flask_login import login_required
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from app import mongo, login_manager
from models import User


index = Blueprint('index', __name__)


@index.route("/")
@index.route("/index")
@login_required
def main():
    # Set Weekend date
    today = date.today()
    sat = today + relativedelta(weekday=5, hour=0, minute=0, second=0)
    sun = today + relativedelta(weekday=6, hour=23, minute=59, second=59)

    # Query
    where = {"hold_date": {'$gte': sat, '$lte': sun}}
    order_by = {'date': 1}, {'place_id': 1}
    query = mongo.db.race_calendar.find()
    print(list(query))

    # Return
    return render_template("index.html", holds=query)


@index.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("images/favicon.ico")
