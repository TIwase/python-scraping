# -*- coding: utf-8 -*-

import re
import ssl
import numpy as np
# import pandas as pd
import urllib
import datetime
from bs4 import BeautifulSoup

# ------------------------------------------------------------------
# メイン関数
def get_covid19():
    all_articles = get_backnums()
    df = []
    for i in range(len(all_articles)):
        for j in range(len(all_articles[i])):
            df.append(scr_covid19(all_articles[i][j]))
    return df

# ------------------------------------------------------------------
# コロナ発生月(3月)から今月までの記事URLを一括取得する関数
def get_backnums():
    dt = datetime.datetime.now()
    year = dt.year
    firstMonth = '03'
    curMonth = dt.strftime('%m') # 0埋めした2桁の10進数で表した月
    nums = np.arange(int(firstMonth), int(curMonth) + 1) # 3月から今月までの配列を生成
    nums = np.sort(nums)[::-1] # 降順にソート
    months = ['0' + str(num) for num in nums] # 0埋めした2桁の10進数に直す
    all_backnums = []
    
    for i in range(len(months)):
        all_backnums.append(scr_mhlw_articles(year, months[i]))
    
    return all_backnums
# ------------------------------------------------------------------
# 月毎の記事URLを取得する関数
def scr_mhlw_articles(year,month):
    url = 'https://www.mhlw.go.jp/stf/houdou/houdou_list_{}{}.html'.format(year, month)
    ssl._create_default_https_context = ssl._create_unverified_context # 403errorを回避
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html,'html.parser')
    listtag = soup.find_all("li") # htmlのlistタグの抽出
    all_data = [s.contents[0] for s in listtag] 
    elements = re.split('<span>|</span>',str(all_data))
    articles = []
    for i in range(len(elements)):
        if re.search("新型コロナウイルス感染症の現在の状況", elements[i]):
           articles.append(elements[i-1])

    backnumbers = []
    for line in articles:
        backnumbers.append(re.search('/stf/newpage_\d+.html', line).group())
    
    return backnumbers
# ------------------------------------------------------------------
# 国別および都道府県別のコロナウイルス感染者数を取得する関数
def scr_covid19(article):
    url = 'https://www.mhlw.go.jp' + article
    ssl._create_default_https_context = ssl._create_unverified_context # 403errorを回避
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html,'html.parser')
    tdtag = soup.find_all("td") # htmlのtdタグのみ抽出
    all_data = [s.contents[0] for s in tdtag]
    data = []
    # 余計な文字列を削除してdataに格納
    if re.search('游ゴシック', str(all_data)):
        elements = re.split('<strong>|<font color="#000000" face="游ゴシック">|</font>|</strong>',str(all_data))
    else:
        elements = re.split('\'|<strong>|</strong>|<u>|</u>|</font>|<font size="2"><font size="3">|<sup>※</sup>|名', str(all_data))
    pref_raw = []
    del elements[0]
    if elements[-1] == ']':
        del elements[-1]
    else:
        pref_raw.append(re.split("'|,",elements[-1]))
    
    for i in range(len(elements)):
        if re.match(r'\\n|,', elements[i]) or elements[i] == '' or re.search('国民の皆様へのメッセージ', elements[i]):
            continue
        else:         
            fullwidth = "０１２３４５６７８９"
            if re.search(elements[i], fullwidth): # 全角表記の文字列を半角に変換
                data.append(trans_char(re.search(elements[i], fullwidth).group()))
            else:
                if re.match('人数（', elements[i]):
                    data.append('人数')
                elif re.match('）', elements[i]):
                    continue
                elif re.match('チャーター便|新No.', elements[i]): # チャーター便帰国者による感染者情報と3月6日以前のデータは考慮しない
                    break
                else:
                    data.append(elements[i])

    if len(pref_raw) != 0:
        for var in pref_raw[0]:
            if re.match(r'\s|]', str(var)) or var == '':
                continue
            else:
                data.append(var)

    return data
# ------------------------------------------------------------------
# 全角->半角に変換する関数
def trans_char(text):
    # 以下の全角文字が対象    
    # text = "！＂＃＄％＆＇（）＊＋，－．／０１２３４５６７８９：；＜＝＞？＠ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ［＼］＾＿｀>？＠ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ｛｜｝～"
    halfwidth = text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    return halfwidth

def get_pref():
    all_pref = ['北海道','青森','岩手','宮城','秋田','山形','福島','茨城','栃木','群馬','埼玉','千葉','東京','神奈川','新潟','富山','石川','福井','山梨','長野','岐阜','静岡','愛知','三重','滋賀','京都','大阪','兵庫','奈良','和歌山','鳥取','島根','岡山','広島','山口','徳島','香川','愛媛','高知','福岡','佐賀','長崎','熊本','大分','宮崎','鹿児島','沖縄']
    return all_pref
