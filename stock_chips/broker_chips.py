import requests
from bs4 import BeautifulSoup
import pandas as pd
# import mssql.mssql_control as mssql
import datetime
date_1 = '2016-01-04'
date_2 = str(datetime.date.today())
ID_NO = '2330'
url = """https://www.nvesto.com/tpe/"""+ID_NO+"""/majorForce#!/fromdate/"""+date_1+"""/todate/"""+date_2+"""/view/summary"""  

url_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
r = requests.post(url, headers=url_headers)

r.encoding = "utf-8"
soup = BeautifulSoup(r.text, "html.parser")
table = soup.find('div', attrs={'class': 'row'})
print(table)
# table = pd.read_html(str(table))[0]
print(table)
table = soup.find('table', attrs={'class': 'table table-bordered'})
table = pd.read_html(str(table))[0]
print(table)


title = table.find(
    'span', {'style': 'color:blue;font-size:14pt;font-weight:bold;'})
title = title.text + '-億元'
print(title)
title_no = title[0:4]
# print(title_no)
items = soup.find('table', {'class': 'solid_1_padding_4_4_tbl'})
