import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


"""
    個股日成交資訊-歷史資料
"""

"""
    1. 爬蟲相關搜集所需歷史資料
    定義資料時間轉換，因台灣證交所提供資料是民國計算
"""


def transform_data(data):
    y, m, d = data.split('/')
    return str(int(y) + 1911) + '-' + m + '-' + d


"""
    2. 爬蟲相關搜集所需歷史資料
    某些瀏覽器會偵測爬蟲，所以先假裝真人myHeader
"""
myHeader = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


def get_data(begin, stocks):
    print('開始搜集資料...')
    "(1). 目標網址"
    baseurl = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date={}&stockNo={}".format(begin, stocks)

    "(2) content 可以解決某些回傳失敗問題"
    data = requests.get(url=baseurl, headers=myHeader).content
    title = BeautifulSoup(data, 'html.parser').find('thead').find('tr')

    "(3)處理資料 組成表格"
    dataList = []
    for col in title.find_all_next('tr'):
        dataList.append([row.text for row in col.find_all('td')])
    # print(dataList)

    # 刪除第一行不需要的資料
    for each in dataList[1:]:
        each[0] = transform_data(each[0])

    # 將資料格式轉換成pandas的DataFrame
    df = pd.DataFrame(dataList[1:], columns=dataList[:1])
    df.columns = dataList[0]

    # print('{} {} 資料搜集成功!! YA'.format(stocks, begin))

    return df


"""
    3. 儲存為csv
"""


def data_to_csv(input_df, stocks):
    # 確認股票是否存在
    if os.path.isfile('./csvFile/{}.csv'.format(stocks)):
        # 避免異常，檢查資料
        try:
            cu_data = pd.read_csv('./csvFile/{}.csv'.format(stocks))
            if input_df['日期'][0] in list(cu_data['日期']):
                print('資料檢查結果：有重複資料...不重複寫入')
                time.sleep(1)
            else:
                input_df.to_csv('./csvFile/{}.csv'.format(stocks), mode='a', header=False)
                time.sleep(1)
            print('寫入完成!YA')
        except Exception as e:
            print('有某步驟錯誤，請檢查CODE:' + str(e))

    else:
        print('資料檢查結果：無重複資料...創建新資料寫入中')

        # 寫入csv
        input_df.to_csv('./csvFile/{}.csv'.format(stocks), mode='w')
        time.sleep(5)


"""
    4. 定義時間區間
    start_year 開始年
    start_month 開始月
    end_year 結束年
    end_month 結束月
"""


def diff_datetime(start_year, start_month, end_year, end_month):
    # 產生年份清單
    year_list = []
    for i in range(end_year - start_year + 1):
        year_list.append(start_year + i)
    whole_date = []
    for strtime in year_list:
        # 因為開始與結束年的月份不一定剛好是12個月，故要另外處理
        if strtime == start_year:
            # 處理開始年的月份
            # 月份小於10，需要在前面位數補0，例如：3月要填03
            for mon in range(start_month, end_month + 1):
                if mon > 9:
                    str_sm = mon
                    whole_date.append('{}{}01'.format(strtime, str_sm))
                elif mon <= 9:
                    str_sm = '0{}'.format(mon)
                    whole_date.append('{}{}01'.format(strtime, str_sm))
                else:
                    print('請輸入正確的月份：(1-12)')

        # 照上面的邏輯再操作一次，處理結束年、月的資料
        elif strtime == end_year:
            # 處理結束年的月份
            for mon in range(1, end_month + 1):
                if mon > 9:
                    end_sm = mon
                    whole_date.append('{}{}01'.format(strtime, end_sm))
                elif mon <= 9:
                    end_sm = '0{}'.format(mon)
                    whole_date.append('{}{}01'.format(strtime, end_sm))
                else:
                    print('請輸入正確月份：(1-12)')
            else:
                for nor_mon in range(1, 13):
                    if nor_mon > 9:
                        nor_m = nor_mon
                        whole_date.append('{}{}01'.format(strtime, nor_m))
                    elif nor_mon <= 9:
                        whole_date.append('{}0{}01'.format(strtime, nor_mon))
                    else:
                        print('請輸入正確月份：(1-12)')

    return whole_date


