# -*- coding: utf-8 -*-
import os
import re
from selenium import webdriver
import datetime
import time

# 全商品情報を取得する
def getProd():
    # 順に, ネオン/グレー/ターコイズ(Lite)/コーラル(Lite)/グレー(Lite)/イエロー(Lite)/どう森セット
    amazonURL = ['https://www.amazon.co.jp/dp/B07WXL5YPW/ref=cm_sw_em_r_mt_dp_U_leuPEbWA5BA5D'
             ,'https://www.amazon.co.jp/dp/B07WS7BZYF/ref=cm_sw_em_r_mt_dp_U_wfuPEbDRAW5AC'
             ,'https://www.amazon.co.jp/dp/B07X779ZK5/ref=cm_sw_em_r_mt_dp_U_aouPEbKVFHQW3'
             ,'https://www.amazon.co.jp/dp/B085GGZ5GS/ref=cm_sw_em_r_mt_dp_U_npuPEb87YGD4G'
             ,'https://www.amazon.co.jp/dp/B07X47QTN3/ref=cm_sw_em_r_mt_dp_U_QpuPEbKYDSHTX'
             ,'https://www.amazon.co.jp/dp/B07X24S7DY/ref=cm_sw_em_r_mt_dp_U_kquPEbJ0YPMKR'
             ,'https://www.amazon.co.jp/dp/B084HPMVNN/ref=cm_sw_em_r_mt_dp_U_hqwPEbMYC08PG'] 
    
    rakutenURL = ['https://books.rakuten.co.jp/rb/16033028/?bkts=1&l-id=search-c-item-text-05'
                  ,'https://books.rakuten.co.jp/rb/16033027/?bkts=1'
                  ,'https://books.rakuten.co.jp/rb/16039046/?bkts=1&l-id=search-c-item-text-02'
                  ,'https://books.rakuten.co.jp/rb/16247998/?bkts=1&l-id=search-c-item-text-07'
                  ,'https://books.rakuten.co.jp/rb/16039045/?bkts=1&l-id=search-c-item-text-04'
                  ,'https://books.rakuten.co.jp/rb/16039044/?bkts=1&l-id=search-c-item-text-03'
                  ,'https://books.rakuten.co.jp/rb/16247994/?bkts=1&l-id=search-c-item-text-09']
    
    sevenURL = ['https://7net.omni7.jp/detail/2110613607'
                ,'https://7net.omni7.jp/detail/2110595636'
                ,'https://7net.omni7.jp/detail/2110613617'
                ,'https://7net.omni7.jp/detail/2110615298'
                ,'https://7net.omni7.jp/detail/2110613616'
                ,'https://7net.omni7.jp/detail/2110613615']
    
    msg_arr = []
    for i in range(len(amazonURL)): 
        msg_arr.append(scrAmazon(amazonURL[i]))
    for i in range(len(rakutenURL)): 
        msg_arr.append(scrRakuten(rakutenURL[i]))    
    for i in range(len(sevenURL)): 
        msg_arr.append(scrSeven(sevenURL[i]))     
    
    return msg_arr

# ------------------------------------------------------------------
# 単一の商品ページの価格および在庫状況を取得する
### Amazon.co.jp ###
def scrAmazon(url):
    browser = webdriver.Chrome(os.path.basename('chromedriver.exe'))
    browser.get(url)
    prodName = browser.find_element_by_xpath("//*[@class='a-size-large']").text
    prodPrice = browser.find_element_by_xpath("//*[@class='a-section a-spacing-small']").text
    browser.quit()
    price_arr = re.split(r'\s', prodPrice)
    msgDate = ''
    msgProd = ''
    msgPrice = ''
    msgURL = ''
    
    if len(price_arr) > 4:
        if re.search('\d\d+', str(price_arr[3])):
            dt = datetime.datetime.now()
            msgDate = dt.strftime("%Y-%m-%d %H:%M:%S") + ' 現在\n'
            msgProd = prodName + '  在庫あり。\n'
            msgPrice = '現在の価格は ' + str(price_arr[3]) + ('(') + str(price_arr[0]) + str(price_arr[1]) + ')です。'
            msgURL = url
            
    return (msgDate + msgProd + msgPrice + msgURL)

### 楽天 ###
def scrRakuten(url):
    browser = webdriver.Chrome(os.path.basename('chromedriver.exe'))
    browser.get(url)
    prodName = re.sub(r'\n\S*\s(\S*\s\S*|\S*)',"",browser.find_element_by_id('productTitle').text)
    price = browser.find_element_by_xpath("//*[@class='price']").text
    status = browser.find_element_by_xpath("//*[@class='status']").text
    browser.quit()
    msgDate = ''
    msgProd = ''
    msgPrice = ''
    msgURL = ''
    
    if status != 'ご注文できない商品*':
        dt = datetime.datetime.now()
        msgDate = dt.strftime("%Y-%m-%d %H:%M:%S") + ' 現在\n'
        msgProd = prodName + '  在庫あり。\n'
        msgPrice = '現在の価格は ' + price + ' です。'
        msgURL = url
    
    return (msgDate + msgProd + msgPrice + msgURL)

### セブンネット ###
def scrSeven(url):
    browser = webdriver.Chrome(os.path.basename('chromedriver.exe'))
    browser.get(url)
    time.sleep(1)
    prodName = browser.find_element_by_xpath('//h1[@class="h1ProductName"]').text
    price = browser.find_element_by_xpath('//*[@class="js-productInfoPriceTax"]').text
    try:
        browser.find_element_by_xpath('//input[@value="カートに入れる"]').text
        statusFlag = 0
    except:
        statusFlag  = 1
    
    browser.quit()
    msgDate = ''
    msgProd = ''
    msgPrice = ''
    msgURL = ''
    
    if statusFlag == 0:
        dt = datetime.datetime.now()
        msgDate = dt.strftime("%Y-%m-%d %H:%M:%S") + ' 現在\n'
        msgProd = prodName + '  在庫あり。\n'
        msgPrice = '現在の価格は ' + price + '(税込み)' + ' です。'
        msgURL = url
    
    return (msgDate + msgProd + msgPrice + msgURL)