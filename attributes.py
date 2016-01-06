import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from random import randint
import csv
import datetime
import time
import socket
import pymysql
import re

def getFans(url):
    result = []
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        fans_list = bsObj.find_all("a", {"href": re.compile(r'.fans')})
        fans = fans_list[0].getText()
        friends_list = bsObj.find_all("a", {"href": re.compile(r'.friends')})
        friends = friends_list[0].getText()
        jifen_list = bsObj.find_all("a", {"href": "/jifen/product/lists"})
        jifen = jifen_list[0].getText().strip()
        daren_flag = '#'
        daren_title = '#'
        daren_flag_list = bsObj.find_all("a", {"href": "/user/prodesc"})
        if len(daren_flag_list) >0:
            daren_flag = 'C'
            daren_title_list = bsObj.find_all("span", {"class": "fss inblok fcc"})
            daren_title = daren_title_list[0].getText()
        result.append(fans)
        result.append(friends)
        result.append(jifen)
        result.append(daren_flag)
        result.append(daren_title)
        print(result)
        return result
    except AttributeError as e:
        return None

# Breadmum u30362766298239
# American u35246655713154
getFans("http://www.douguo.com/u/u35246655713154.html")
