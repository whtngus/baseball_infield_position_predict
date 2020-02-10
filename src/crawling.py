#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os
import csv

crawler_datas = []
split_tag = ".jpg"
start_tag = "http:"
write_path = "../data/crawl/fut/"
load_path = "../crawl/raw_data/FUT_raw"
write_file_name = "fut.csv"

with open(load_path, "r", encoding="utf-8") as f:
    crawler_datas = f.readlines()
    f.close()

# test_urls = ["//crdfcowjurxm984864.cdn.ntruss.com/person/middle/2019/76232.jpg선수명: 양의지등번호: No.25생년월일: 1987년 06월 05일포지션: 포수(우투우타)신장/체중: 179cm/85kg경력: 송정동초-무등중-진흥고-두산-경찰-두산입단 계약금: 3000만원연봉: 200000만원지명순위: 06 두산 2차 8라운드 59순위입단년도: 06두산"]
user_historys = []
for test_url in crawler_datas:
    user_history = {}
    url = start_tag + test_url.split(split_tag)[0] + split_tag
    test_url = test_url.split("선수명:")[1].split("등번호:")
    player_name = test_url[0].strip()
    user_history["name"] = player_name
    test_url = test_url[1][4:].split("생년월일: ")
    user_history["number"] = test_url[0]
    test_url = test_url[1].split("포지션: ")
    user_history["berth"] = test_url[0]
    test_url = test_url[1].split("신장/체중: ")
    user_history["position"] = test_url[0]
    test_url = test_url[1].split("cm/")
    user_history["height"] = test_url[0]
    test_url = test_url[1].split("경력: ")
    user_history["weight"] = test_url[0].split("kg")[0]
    test_url = test_url[1].split("만원연봉: ")
    if len(test_url) == 1:
        user_history["payment"] = 0
        test_url = test_url[0].split("연봉: ")
    else:
        user_history["payment"] = test_url[0].split("계약금: ")[1]
    if len(test_url) == 2 and  "만원지명순위:" in test_url[1]:
        user_history["salary"] = test_url[1].split("만원지명순위:")[0]
    else:
        user_history["salary"] = 0
    os.system("wget " + url + " -O " + write_path + player_name +".jpg")
    user_historys.append(user_history)


with open(write_path + write_file_name,"w",encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=user_historys[0].keys())
    writer.writeheader()
    for user_history in user_historys:
        writer.writerow(user_history)

