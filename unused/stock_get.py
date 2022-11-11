import requests
from bs4 import BeautifulSoup
#原版
# GoodInfo損益表--累計季表url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp"url_paras = {'RPT_CAT': 'IS_M_QUAR_ACC', 'STOCK_ID': '2330'}

# url_headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
# r = requests.get(url, params=url_paras, headers=url_headers)
# r.encoding = "utf-8"
# soup = BeautifulSoup(r.text, "lxml")
# print(soup)

#新版
# GoodInfo損益表--累計季表url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp"url_paras = {'RPT_CAT': 'IS_M_QUAR_ACC', 'STOCK_ID': '2330'}
url = 'https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=2409'
url_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
r = requests.get(url, params=url_paras, headers=url_headers)
r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "lxml")
print(soup)