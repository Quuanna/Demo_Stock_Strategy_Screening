import time
import os
import schedule
from datetime import datetime
import stockHistoryData as stock
import stockMplfinance as mplf
import lineNotifySchedule as notify
import stockFilterMenuData as menu

"""
    盤後四點觸發
    1. 篩選 ex: code = ['1304']
    2. 取得3個月的個股歷史資料
"""


def old_remove_file(code):
    # 舊的需刪除
    for i in code:
        try:
            fileTest = r"./csvFile/{}.csv'".format(i)
            os.remove(fileTest)
        except OSError as e:
            print(e)
        else:
            print("File is deleted successfully")


def get_csv_file():
    code = menu.get_stock_menu()
    # 取新的
    cralwer_date = stock.diff_datetime(2022, 5, 2022, 8)
    for sn in code:
        print('[{}]'.format(sn))
        for dn in cralwer_date:
            stock.data_to_csv(stock.get_data(dn, sn), sn)
            time.sleep(5)
    return code



"""
    3. 視覺畫圖表 
    4. Line notify
"""
token = 'Z70aV1naXQTShh0qtcEpot1BzYIFYVFnea9WMVKS0QU'  # 個人


# token = 'ccOMq7oiDs6pfLyjtigexcKCelDRrSeepZxmunXMSAw'  # 群組


def send_before(code):
    for i in code:
        stockCsv = './imgCsvFile/{}.csv'.format(i)
        image = './image/{}image.png'.format(i)
        mplf.set_data_frame('./csvFile/{}.csv'.format(i)).to_csv(stockCsv)

        if mplf.set_mplfinance_to_image(i, stockCsv) == i:
            set_before_msg = "盤前看個股 => \n https://www.twse.com.tw/pdf/ch/{}_ch.pdf".format(i)
            notify.send_message(token, set_before_msg, "")


def send_after(code):
    for i in code:
        stockCsv = './imgCsvFile/{}.csv'.format(i)
        image = './image/{}image.png'.format(i)
        mplf.set_data_frame('./csvFile/{}.csv'.format(i)).to_csv(stockCsv)

        if mplf.set_mplfinance_to_image(i, stockCsv) == i:
            set_after_msg = "投信買超股＋成交破前量的股票 = [{}]".format(i)
            notify.send_message(token, set_after_msg, image)


# 測試
# get_csv_file()
# send_after(get_csv_file())

send_before(get_csv_file())
# send_after(get_csv_file())

schedule.clear()
schedule.every().day.at('08:00').do(send_before(get_csv_file()))  # 盤前
schedule.every().day.at('13:30').do(old_remove_file(get_csv_file()))  # 盤後前先刪除資料
schedule.every().day.at('16:00').do(send_after(get_csv_file()))  # 盤後先取資料

while True:
    print('schedule running.....')
    schedule.run_pending()
