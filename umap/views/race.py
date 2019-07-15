from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app import mongo, login_manager

import re
import json
import bs4 as bs
from requests import Session, HTTPError
from datetime import datetime

race = Blueprint('race', __name__, url_prefix='/race')


@race.route('/', methods=["GET", "POST"])
@login_required
def main():
    if request.method == "GET":
        user_info = "(ﾟ∀ﾟ)ﾗｳﾞｨ!!"
        return render_template("race_all.html", user=user_info)
    else:
        # Convert JSON to DICT
        data = json.loads(request.data)
        mongo.db.races.update({"_id": data["_id"]}, data, upsert=True)
    return jsonify({"message": "SUCCESS"}), 200


@race.route('/<string:race_id>', methods=["GET"])
@login_required
def get(race_id):
    # Create Netkeiba URL
    base_url = "https://race.netkeiba.com/?pid=race_old&id=c"
    url = base_url + race_id

    # Get HTML
    soup = get_soup(url)
    if soup.find("table", {"class": "race_table_old"}) is not None:
        race = race_to_json(race_id, soup)
        return race, 200
    else:
        return jsonify({"message": "There is No Entry"}), 500


def get_soup(_url):
    """HTML取得
    引数で与えられたURLのHTMLを取得してBeautiful Soupクラスで返すファンクション
    """
    try:
        session = Session()
        html = session.get(_url)
        soup = bs.BeautifulSoup(html.content, "html.parser")
    except HTTPError as e:
        print("HTTP error: {0}".format(e))
        raise
    return soup


def race_to_json(race_id, _soup):
    """取得したレース出走情報のHTMLから辞書を作成
    netkeiba.comのレースページから情報をパースしてjson形式で返すファンクション
    """
    race = {}

    # Extract race data
    base = _soup.find("div", {"class": "data_intro"})

    race["_id"] = race_id
    race["round"] = int_fmt(base.find("dt").string, "\d+")
    race["title"] = str_fmt(base.find("h1").text, "[^!-~\xa0]+")

    attrs = base.find("dd").find_all("p")
    tm = str_fmt(attrs[1].string, "\d{2}:\d{2}")
    race["course"] = str_fmt(attrs[0].string, "芝|ダ|障")
    race["distance"] = int_fmt(attrs[0].string, "\d{4}")
    race["weather"] = str_fmt(attrs[1].string, "晴|曇|小雨|雨|小雪|雪")
    race["going"] = str_fmt(attrs[1].string, "良|稍重|重|不良")

    attrs = base.find("div", {"class": "race_otherdata"}).find_all("p")
    dt = re.sub("/", "-", str_fmt(attrs[0].string, "\d{4}/\d{2}/\d{2}"))
    race["race_date"] = dt + "T" + tm + ":00.000Z"
    race["place"] = race_id[4:6]
    race["count"] = int_fmt(attrs[2].string, "\d+")
    race["max_prize"] = int_fmt(attrs[3].string, "\d+")

    table = _soup.find("table",  {"class": "race_table_old"})
    race["horse"] = table_to_list(table)

    # Dict to JSON
    json_race = json.dumps(race)

    return json_race


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
            h["horse_id"] = str_fmt(cell[num["馬名"]].a.get("href"), "\d+")
            h["burden"] = float_fmt(cell[num["負担重量"]].string, "\d+.\d+")
            h["jockey_id"] = str_fmt(cell[num["騎手"]].a.get("href"), "\d+")
            h["owner_id"] = str_fmt(cell[num["厩舎"]].a.get("href"), "\d+")
            h["weight"] = int_fmt(cell[num["馬体重"]].string, "(\d+)\([+-]?\d*\)")
            h["diff"] = int_fmt(cell[num["馬体重"]].string, "\d+\(([+-]?\d+)\)")
            entry.append(h)

    return entry


def int_fmt(_target, _reg):
    val = check_format(_target, _reg)
    val = int(re.sub(",", "", val)) if val is not None else 0

    return val


def float_fmt(_target, _reg):
    val = check_format(_target, _reg)
    val = float(re.sub(",", "", val)) if val is not None else 0

    return val


def str_fmt(_target, _reg):
    val = check_format(_target, _reg)
    val = str(val) if val is not None else ""

    return val


def check_format(_target, _reg):
    # check target variables
    fmt = re.compile(_reg)
    if _target is not None and fmt.search(_target):
        val = fmt.findall(_target)[0]
    else:
        val = None

    return val
