from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from flask import Blueprint, current_app, render_template
from flask_login import login_required
from flask_pymongo import ASCENDING, DESCENDING

from app import login_manager, mongo
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
    where = {"hold_date": {"$gte": sat, "$lte": sun}}
    order_by = [('hold_date', DESCENDING), ('place_name', ASCENDING)]
    query = mongo.db.holds.find(where).sort(order_by)

    # Return
    return render_template("index.html", holds=query)


@index.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("images/favicon.ico")
