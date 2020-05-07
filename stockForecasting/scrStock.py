# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:11:03 2020
"""
import re
import ssl
import numpy as np
import pandas as pd
import urllib
import datetime
from bs4 import BeautifulSoup

# ------------------------------------------------------------------
def get_stock(code, fromYear, toYear):
    if fromYear == toYear: # 指定した1年間分の株価を取得
        year = fromYear
        df = scr_stock(code, year)   
    else: # 指定した数年間分の株価を取得
        arrYear = np.arange(fromYear, toYear + 1) # fromYear以上、toYear以下の数値を配列に代入
        all_df = []
        for i in range(len(arrYear)):
            all_df.append(scr_stock(code, arrYear[i]))
        df = pd.concat([all_df[i] for i in range(len(arrYear))])

    return df
# ------------------------------------------------------------------
# 1年間分の株価を取得する関数
def scr_stock(code, year):
    url = 'https://kabuoji3.com/stock/{}/{}/'.format(code, year)
    ssl._create_default_https_context = ssl._create_unverified_context # 403errorを回避
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html,'html.parser')
    # print(soup.prettify())  # 読み込んだhtmlソースを表示
    tdtag = soup.find_all("td") # htmlのtdタグのみ抽出
    all_stock = [s.contents[0] for s in tdtag]
    all_stock = list(zip(*[iter(all_stock)]*7)) # 7列に整形
    elements = str(all_stock).split(',')
    dateCol = []
    openCol = []
    highCol = []
    lowCol = []
    closeCol = []
    volCol = []
    adjcloseCol = []
    
    for i in range(0,len(elements),7):
        dateCol.append(re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',elements[i]).group())
    for i in range(1,len(elements),7):
        openCol.append(re.search("\d+",elements[i]).group())
    for i in range(2,len(elements),7):
        highCol.append(re.search("\d+",elements[i]).group())
    for i in range(3,len(elements),7):
        lowCol.append(re.search("\d+",elements[i]).group())
    for i in range(4,len(elements),7):
        closeCol.append(re.search("\d+",elements[i]).group())
    for i in range(5,len(elements),7):
        volCol.append(re.search("\d+",elements[i]).group())
    for i in range(6,len(elements),7):
        adjcloseCol.append(re.search("\d+",elements[i]).group())
    
    stock = np.c_[dateCol,openCol,highCol,lowCol,closeCol,volCol,adjcloseCol]
    df = pd.DataFrame(stock,)
    df.columns=['日付','始値','高値','安値','終値','出来高','終値調整値']
    
    return df

