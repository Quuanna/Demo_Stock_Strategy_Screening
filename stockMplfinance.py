import os
import time
import pandas as pd
import numpy as np
import mplfinance as mplf
import csv
from datetime import datetime

"""
    個股日成交資訊-繪圖
"""

""" 1. 讀取 CSV 資料 / 處理表格所需資料 / DataFrame 做表格 
    readFile 外部給Csv資料
    return df 給外部已經轉化表格的資料
"""


def set_data_frame(read_file):
    if os.path.isfile(read_file):
        # 避免異常，檢查資料
        try:
            # 處理表格所需資料
            date1 = []
            open1 = []
            high = []
            low = []
            close = []
            Volume = []

            with open(read_file, newline='') as csvfile:
                rows = csv.DictReader(csvfile)
                for row in rows:
                    # 指定要的項目
                    date1.append((row['日期']))
                    open1.append((float(row['開盤價'])))
                    high.append((float(row['最高價'])))
                    low.append((float(row['最低價'])))
                    close.append((float(row['收盤價'])))
                    Volume.append(float(row['成交股數'].replace(',', '')))  # 去掉千分位

            # 製作表格
            index = {
                "Date": date1
            }
            stockList = {
                "Open": open1,
                "High": high,
                "Low": low,
                "Close": close,
                "Volume": Volume
            }
            dfNum = pd.DataFrame(index)
            df = pd.DataFrame(stockList, index=dfNum['Date'])  # index 指定
            return df


        except Exception as e:
            print('檢查資料錯誤:' + str(e))
    else:
        print('檢查無檔案...')


""" 2. mplfinance 繪圖"""


def set_mplfinance_to_image(code, csv_file_str):
    if os.path.isfile(csv_file_str):
        try:
            csvFile = csv_file_str
            readData = pd.read_csv(csvFile)
            readData.Date = pd.to_datetime(readData.Date)
            data = readData.set_index('Date')

            # 畫K棒的顏色
            # up='r' 漲時紅色 、 down='g' 跌時綠色
            mc = mplf.make_marketcolors(up='r',
                                        down='g',
                                        edge='',
                                        wick='inherit',
                                        volume='inherit')

            # 畫線
            two_points = set_alines(readData)

            # 設定 mplfinance 樣式
            style = mplf.make_mpf_style(
                base_mpf_style='yahoo',
                marketcolors=mc)

            # 發送
            mplf.plot(data,
                      title='{} 2022-05 ~ 2022-8'.format(code),
                      mav=(5, 10, 20),
                      type='candle',
                      alines=dict(alines=two_points, colors=['b']),
                      datetime_format='%m-%d',
                      ylabel='Price ($)',
                      style=style,
                      volume=True,  # volume 顯示成交股數
                      savefig='./image/{}image'.format(code))  # savefig 儲存 png

            # mplf.show()

        except Exception as e:
            # print('                    ')
            print('檢查資料錯誤:' + str(e))
    else:
        print(' mplfinance 繪圖 - 檢查無檔案...')

    return code


"""3. 畫線
    (1.) 空轉多下降切線：畫線找到第一高點和第二高點，判斷時間點
    (2.) 多轉空上升切線：找到第一低點和第二低點，，判斷時間點
ex: two_points  = [底點('2016-05-19',203.5),高點('2016-05-25',209.5)]

"""


# 處理日期格式 yyyy-mm-dd
def transform_data(data):
    y, m, d = data.split('-')
    return m + "/" + d + "/" + y


high = []
low = []


def set_alines(df):
    # 轉換index
    dfList = df.reset_index()
    high = np.argmax(df.get('High'))
    low = np.argmin(df.get('Low'))
    lowDate = dfList.iloc[low, :]['Date']
    lowPoint = dfList.iloc[low, :]['Low']
    highDate = dfList.iloc[high, :]['Date']
    highPoint = dfList.iloc[high, :]['High']

    # print('畫線：', [(lowDate, lowPoint), (highDate, highPoint)])
    nowtime = datetime.now()
    # print("比較差一個月={}".format(type((nowtime - lowDate).days)))

    if lowDate > highDate:

        if ((nowtime - lowDate).days) < 40:
            return [(lowDate, lowPoint), (highDate, highPoint)]
