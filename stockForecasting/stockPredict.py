# -*- coding: utf-8 -*-
import os
from fbprophet import Prophet
from scraping import get_stock

# "株式投資メモ"のサイトから株価データを参照
# 株価データの読み込み形式を下記1,2どちらかを選択すること
# ------------------------------------------------------------------
code = 6758 # 銘柄コード
fromYear = 2020
toYear = 2020


# 1) CSVファイルから読み込む場合
# df = pd.read_csv(os.path.basename('{}_{}.csv'.format(code,year)) ,encoding='cp932', skiprows=1)

# 2) HTML上の株価をスクレイピングする場合
df = get_stock(code, fromYear, toYear)

# print(type(df))
# ------------------------------------------------------------------
close = df.iloc[:,[0,4]]  # '日付'と'終値'を抽出
data = close.rename(columns={'日付':'ds', '終値':'y'})
model = Prophet()
# model = Prophet(seasonality_mode='multiplicative')
model.fit(data)
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)
model.plot(forecast)
model.plot_components(forecast)

