import csv

import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from numpy import genfromtxt
from pandas import read_csv

"""
    篩選投信+外資-股票清單
"""

"(1). 假裝真人myHeader"
myHeader = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_data_list(target, type):
    " (2). 目標網址 "
    baseurl = "https://www.twse.com.tw/zh/listed/listingProfileInquiry?mobile=&selectItem={}&selectSubitem={}".format(
        target, type)

    "(3).  content 可以解決某些回傳失敗問題 "
    data = requests.get(url=baseurl, headers=myHeader).content
    title = BeautifulSoup(data, 'html.parser').find('thead').find('tr')

    "(4)處理資料 組成表格"
    dataList = []
    for col in title.find_all_next('tr'):
        str = [row.text for row in col.find_all('td')][0]
        dataList.append(re.sub(r"\s+", "", str))  # 去掉字串中所有的空格/空白符
    # print(dataList)
    return dataList


"""
    2 成交量 -> 1 成交量增加前 50 名
    3 三大法人 -> 0 投信買超前 50 名
              -> 2 自營商買超前 50 名
              -> 4 外資及陸資買超前 50 名
"""


def get_stock_filter_menu(lst, *lsts):
    sameList = []
    for ist in lsts:
        for element in ist:
            for i in lst:
                if element == i:
                    sameList.append(element)

    return sameList


"""
    當日盤後下午四點時更新儲存資料
"""


def get_stock_menu():
    # 成交量
    volume = get_data_list(2, 1)
    # 投信買超
    letter = get_data_list(3, 0)
    # 外資買超
    foreignInvestment = get_data_list(3, 4)

    letter_buy = get_stock_filter_menu(letter, volume)
    foreignInvestment_buy = get_stock_filter_menu(letter_buy, foreignInvestment)
    letter_foreignInvestment_buy = get_stock_filter_menu(foreignInvestment_buy, volume)
    # print("投信買超 = ", letter_buy)
    # print("外資買超 = ", get_stock_filter_menu(foreignInvestment_buy, volume))
    # print("投信 + 外資 = ", get_stock_filter_menu(letter_buy, foreignInvestment))


    return letter_buy


