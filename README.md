# stockStrategyScreening 

### self project info
此為練習範例，目的是為了學習python所實作範例，主題：投資策略篩選「程式化」結合使用 Line notify 發送通知

需達成原本人在做的事交給程式自動執行，使用市面上常見的投資策略常見規則例如：價格、成較量、財報、即時新聞、技術指標等等，設定排程定期運行選股模型，並透過LINE notify把選股結果推送到LINE上

### implement step 
1. 資料源「台灣證交所公開資訊」
2. 處理資料格式
3. 篩選資料
4. 視覺化資料圖表
5. 設定排程
6. line notify

### import python library use
1. requests先get網頁所有資料
2. BeautifulSoup 對資料解析，使用格式‘html.parser’、網頁特殊字型處理
3. python內建datatime處理時間日期的相關格式，民國轉西元
4. pandas 將搜集資料格式轉換成pandas的DataFrame表格
5. CSV儲存資料
6. mplfinance 繪製視覺化圖表

### 蒐集->篩選->處理資料->繪圖，如「1101 台積電」 
## 經過搜集後整理儲存的 CSV 資料

## 使用CSV資料繪製視覺化資料圖表
