# -*- coding:utf-8 -*-
import re
import pymongo
from dateutil.tz import tzutc
from lxml import etree
from lxml.html import parse
from pandas.util.testing import DataFrame
import pandas as pd
import numpy as np
import requests
import json
from datetime import timedelta, datetime
import arrow
from numpy import interp
import tushare as ts
from PyQt5 import Qt
import sys
import xlrd
import zipfile
import io

api_home = 'http://xueqiu.com'
# check xueqiu HTTP request cookie "xq_a_token"
xq_a_token = '6fe724e8526b1fd63a6390936c5151137479dca9'
headers = {'content-type': 'application/json',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}


# 雪球自选股清单
def parse_stocks(access_token=xq_a_token):
    url = 'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&pid=-5&category=1'
    payload = {'access_token': access_token}

    r = requests.get(url, params=payload, headers=headers)
    # print r
    print(r.json())
    stocks = r.json().get('data').get('stocks')
    print(stocks)
    print(len(stocks))
    for stock in stocks:
        print(stock)
        stock.pop('type')
        stock.pop('remark')
        stock.pop('created')
        print(stock)
        exchange = stock['exchange']
        symbol = stock['symbol']
        if exchange == 'SZ':
            stock['symbol'] = symbol.strip('SZ')+'.SZ'
        elif exchange == 'SH':
            stock['symbol'] = symbol.strip('SH')+'.SH'
        stock.pop('exchange')
    df = pd.DataFrame(stocks)
    cols = ['symbol', 'name']
    df = df.ix[:, cols]
    print(df)
    df.to_excel("output.xlsx", index=False)


if __name__ == '__main__':
    parse_stocks()