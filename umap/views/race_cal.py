import json
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required

from app import mongo, login_manager
from .common import *

race_cal = Blueprint('race_cal', __name__, url_prefix='/race_calendar')


@race_cal.route('/', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "GET":
        user_info = "(ﾟ∀ﾟ)ﾗｳﾞｨ!!"
        return render_template("race_all.html", user=user_info)
    else:
        # Convert JSON to DICT
        data = json.loads(request.data)
        mongo.db.race_calendar.insert(data)
    return jsonify({"message": "SUCCESS"}), 200


@race_cal.route('/<string:year_month>', methods=["GET"])
@login_required
def get(year_month):
    # Check Parameter Format
    if check_format(year_month, "^\d{6}$"):
        year = year_month[0:4]
        month = year_month[4:6]
    else:
        return jsonify({"message": "Invalid argument"}), 500

    # Create Yahoo keiba URL
    url = "https://keiba.yahoo.co.jp/schedule/list/"+year+"/?month="+month

    # Check HTML File
    soup = get_soup(url)
    if soup is not None:
        soup = soup.find("table", {"class": "scheLs"})
    else:
        return jsonify({"message": "HTTP Response Error"}), 500

    # Check table and Return JSON
    if soup is not None:
        race_dict = extract_race_cal(soup, year, month)
        return jsonify(race_dict), 200
    else:
        return jsonify({"message": "There is No Calendar"}), 500


def extract_race_cal(_table, _year, _month):
    """取得したレース・カレンダーのHTMLから辞書を作成
    Yahoo!競馬の日程・結果ページから情報をパースしてdict形式で返すファンクション
    """
    race_cal = []
    yr = int(_year)
    mo = int(_month)

    for row in _table.findAll("tr"):
        cells = row.findAll("td")

        if len(cells) == 3 and cells[0].find("a") is not None:
            race = {}
            dy = int_fmt(cells[0].text, "(\d+)日（[日|月|火|水|木|金|土]）")
            race["_id"] = "20" + str_fmt(cells[0].a.get("href"), "\d+")
            race["hold_date"] = datetime(yr, mo, dy)
            race["place_id"] = race["_id"][4:6]
            race["place_name"] = to_place_name(race["place_id"])
            race["days"] = int(race["_id"][6:8])
            race["times"] = int(race["_id"][8:10])
            race_cal.append(race)

    return race_cal
