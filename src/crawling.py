#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os

test_urls = ["//crdfcowjurxm984864.cdn.ntruss.com/person/middle/2019/76232.jpg선수명: 양의지등번호: No.25생년월일: 1987년 06월 05일포지션: 포수(우투우타)신장/체중: 179cm/85kg경력: 송정동초-무등중-진흥고-두산-경찰-두산입단 계약금: 3000만원연봉: 200000만원지명순위: 06 두산 2차 8라운드 59순위입단년도: 06두산"]
split_tag = ".jpg"
start_tag = "http:"
user_historys = {}
for test_url in test_urls:
    user_history = {}
    url = start_tag + test_url.split(split_tag)[0] + split_tag
    test_url = test_url.split("선수명:")[1].split("등번호:")
    player_name = test_url[0]
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
    user_history["payment"] = test_url[0].split("계약금: ")[1]
    user_history["annual)income"] = test_url[1].split("만원지명순위:")[0]
    os.system("wget " + url + " -O " + player_name +".jpg")
    user_historys[player_name] = user_history



