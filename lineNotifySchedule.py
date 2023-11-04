import os
import requests
import schedule
from datetime import datetime


"""
    Line notify 發送通知
"""


"""
    1. 發送通知
"""
def send_message(token, msg, image):
    # line伺服器位址
    url = "https://notify-api.line.me/api/notify"
    # HTTP 標頭參數與資料
    headers = { "Authorization": "Bearer " + token}
    # 傳送本地圖片
    payload = {'message': msg}

    # 要傳送的圖片檔案
    if image != "":
        if os.path.isfile(image):
            try:
                images = open(image, 'rb')  # 以二進位方式開啟圖片
                files = {'imageFile': images}  # 設定圖片資訊
                request = requests.post(url, headers=headers, params=payload, files=files)
                print(request.status_code, request.text)
            except Exception as e:
                print('檢查資料錯誤:' + str(e))
        else:
            print('發送通知圖片檔案 - 檢查無檔案...')
    else:
        request = requests.post(url, headers=headers, params=payload)
        print(request.status_code, request.text)

