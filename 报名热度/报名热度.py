# -*- coding: utf-8 -*-

import requests

from DBUtil import DBUtil


def run():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    db = DBUtil()

    base_url = "https://api.eol.cn/gkcx/api/?page={}&request_type=1&size=20&sort=view_total&uri=apidata/api/gk/school/lists"
    for i in range(1, 148 + 1):
        url = base_url.format(i)
        resp = requests.get(url, headers=headers)
        item_list = resp.json()["data"]["item"]
        for item in item_list:
            save_data(item, db)


def save_data(item, db):
    data = {
        "name": item["name"],  # 学校名称
        "province_name": item["province_name"],  # 地区名称
        "school_type": item["school_type"],  # 办学类型
        "type": item["type"],  # 院校类型
        "address": item["address"],  # 地址
        "city_name": item["city_name"],  # 城市名
        "f211": item["f211"],  # 1是 2否
        "f985": item["f985"],  # 1是 2否
        "view_month": item["view_month"],  # 月人气
        "view_total_number": item["view_total_number"],  # 总人气
        "view_week": item["view_week"]  # 周人气
    }
    db.insertOne(data, "hot_school")


if __name__ == '__main__':
    run()
