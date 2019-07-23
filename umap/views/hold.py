import re
import json
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import mongo
from .common import get_soup, str_fmt, to_place_name

hold = Blueprint('hold', __name__, url_prefix='/hold')


@hold.route('/', methods=["POST"])
@login_required
def main():
    # Convert JSON to DICT
    holds = json.loads(request.data)
    # Validate Data Types
    for hold in holds:
        hold["hold_date"] = datetime.strptime(hold["hold_date"], "%Y-%m-%d")
        mongo.db.holds.update({"_id": hold["_id"]}, hold, upsert=True)
    return jsonify({"message": "SUCCESS"}), 200


@hold.route('/<string:year_month>', methods=["GET"])
@login_required
def get(year_month):
    # Create Yahoo keiba URL from the argument
    if re.match(r"^\d{6}$", year_month):
        year = year_month[0:4]
        month = year_month[4:6]
        url = "https://keiba.yahoo.co.jp/schedule/list/" + year + "/?month=" + month
    else:
        return jsonify({"message": "Invalid argument"}), 500

    # Check HTML File
    soup = get_soup(url)
    if soup is not None:
        soup = soup.find("table", {"class": "scheLs"})
    else:
        return jsonify({"message": "HTTP Response Error"}), 500

    # Check table and Return JSON
    if soup is not None:
        race_dict = extract_hold(soup, year, month)
        return jsonify(race_dict), 200
    else:
        return jsonify({"message": "There is No Calendar"}), 500


def extract_hold(_table, _year, _month):
    """取得したレース・カレンダーのHTMLから辞書を作成
    Yahoo!競馬の日程・結果ページから情報をパースしてdict形式で返すファンクション
    """
    holds = []

    for row in _table.findAll("tr"):
        cells = row.findAll("td")

        if len(cells) == 3 and cells[0].find("a") is not None:
            hold = {}
            dy = str_fmt(cells[0].text, r"(\d+)日（[日|月|火|水|木|金|土]）").zfill(2)
            hold["_id"] = "20" + str_fmt(cells[0].a.get("href"), r"\d+")
            hold["hold_date"] = _year + "-" + _month + "-" + dy
            hold["place_id"] = hold["_id"][4:6]
            hold["place_name"] = to_place_name(hold["place_id"])
            hold["days"] = int(hold["_id"][6:8])
            hold["times"] = int(hold["_id"][8:10])
            holds.append(hold)

    return holds
