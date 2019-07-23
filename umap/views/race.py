import re
import datetime

from app import mongo
from flask import Blueprint, jsonify, request
from flask_login import login_required

from .common import float_fmt, get_soup, int_fmt, str_fmt, to_course_full

race = Blueprint('race', __name__, url_prefix='/race')


@race.route('/', methods=["POST"])
@login_required
def main():
    """ Reseve JSON and insert database
    """
    # Convert JSON to DICT
    race = request.data
    # Type Casting
    race["race_date"] = datetime.strptime(race["race_date"], "%Y-%m-%d %H:%M")
    # Insert record to Race Document
    mongo.db.races.update({"_id": race["_id"]}, race, upsert=True)
    return jsonify({"message": "SUCCESS"}), 200


@race.route('/<string:race_id>', methods=["GET"])
@login_required
def get(race_id):
    """ Collect and parse race calendar and return JSON
    """
    # Create Netkeiba URL from the argument
    if re.match(r"^\d{12}$", race_id):
        url = "https://race.netkeiba.com/?pid=race_old&id=c" + race_id
    else:
        return jsonify({"message": "Invalid argument"}), 500

    # Check HTML File
    soup = get_soup(url)
    if soup is None:
        return jsonify({"message": "HTTP Response Error"}), 500

    # Check table and Return JSON
    if soup.find("table", {"class": "race_table_old"}) is not None:
        race = soup_to_races(soup, race_id)
        return jsonify(race), 200
    else:
        return jsonify({"message": "There is No Race"}), 500


def soup_to_races(_soup, _race_id):
    """取得したレース出走情報のHTMLから辞書を作成
    netkeiba.comのレースページから情報をパースしてjson形式で返すファンクション
    """
    race = {}

    # Extract race data
    base = _soup.find("div", {"class": "data_intro"})

    race["_id"] = _race_id
    race["round"] = int_fmt(base.find("dt").string, r"\d+")
    race["title"] = str_fmt(base.find("h1").text, r"[^!-~\xa0]+")

    attrs = base.find("dd").find_all("p")
    tm = str_fmt(attrs[1].string, r"\d{2}:\d{2}")
    race["course"] = to_course_full(str_fmt(attrs[0].string, r"芝|ダ|障"))
    race["distance"] = int_fmt(attrs[0].string, r"\d{4}")
    race["weather"] = str_fmt(attrs[1].string, r"晴|曇|小雨|雨|小雪|雪")
    race["going"] = str_fmt(attrs[1].string, r"良|稍重|重|不良")

    attrs = base.find("div", {"class": "race_otherdata"}).find_all("p")
    dt = re.sub("/", "-", str_fmt(attrs[0].string, r"\d{4}/\d{2}/\d{2}"))
    race["race_date"] = dt + " " + tm
    race["place"] = _race_id[4:6]
    race["count"] = int_fmt(attrs[2].string, r"\d+")
    race["max_prize"] = int_fmt(attrs[3].string, r"\d+")

    table = _soup.find("table", {"class": "race_table_old"})
    race["horse"] = table_to_list(table)

    return race


def table_to_list(_table):
    """テーブルから出走情報のリストを作成
    netkeiba.comのレースページの出走情報テーブルからリストを作成するファンクション
    """
    # Get column number of needed columns
    num = {"馬名": 0, "負担重量": 0, "騎手": 0, "厩舎": 0, "馬体重": 0}
    header = [x.text for x in _table.findAll("tr")[0].findAll("th")]
    for key in num:
        num[key] = header.index(key)

    entry = []
    for row in _table.findAll("tr")[2:]:
        h = {}
        cell = row.findAll("td")

        if len(cell) > 0:
            h["horse_id"] = str_fmt(cell[num["馬名"]].a.get("href"), r"\d+")
            h["burden"] = float_fmt(cell[num["負担重量"]].string, r"\d+.\d+")
            h["jockey_id"] = str_fmt(cell[num["騎手"]].a.get("href"), r"\d+")
            h["owner_id"] = str_fmt(cell[num["厩舎"]].a.get("href"), r"\d+")
            h["weight"] = int_fmt(cell[num["馬体重"]].string,
                                  r"(\d+)\([+-]?\d*\)")
            h["diff"] = int_fmt(cell[num["馬体重"]].string, r"\d+\(([+-]?\d+)\)")
            entry.append(h)

    return entry
