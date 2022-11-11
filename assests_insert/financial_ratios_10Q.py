import requests
from bs4 import BeautifulSoup
import pandas as pd
import mssql.mssql_control as mssql


def insert_ratio(ID_NO):
    url = """https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID="""+ID_NO+""""""
    url_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    r = requests.post(url, headers=url_headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    #table = soup.find('table', attrs={'class': 'solid_1_padding_6_2_tbl'})
    table = soup.find('table', attrs={'class': 'b1 p6_0 r10_0'})
    title = table.find(
        'span', {'style': 'color:blue;font-size:14pt;font-weight:bold;'})
    title = title.text + '-%'
    print(title)
    title_no = title[0:4]
    # print(title_no)
    #items = soup.find('table', {'class': 'solid_1_padding_4_4_tbl'})
    items = soup.find('table', {'class': 'b1 p4_4 r0_10 row_mouse_over'})
    table = pd.read_html(str(items))[0]  # 將table直接轉dataframe
    # 先檢查資料表balance_Assets,balance-debt,balance_Equity存不存在,並且添加
    cursor = mssql.conneected()
    table_name = {
        'rate_profit_ability': '獲利能力',
        'rate_profit_year_growth': '獲利年成長',
        'rate_in_total_assets': '各項資產佔總資產比重',
        'rate_quarterly_growth': '資產季成長率',
        'rate_year_growth': '資產年成長率',
        'rate_debt_equity_in_total_assets': '負債&股東權益佔總資產',
        'rate_debt_equity_increase_decrease_quarterly': '負債&股東權益季增減率',
        'rate_debt_equity_increase_decrease_year': '負債&股東權益年增減率',
        'rate_debt_payment': '償債能力',
        'rate_management_capacity': '經營能力',
        'rate_cash_flow_position': '現金流量狀況',
        'rate_other_index': '其他指標',
    }
    for key, _ in table_name.items():
        mssql.create(key, cursor)
    # 20200221寫到這
    # 檢查表單欄位存不存在,並添加
    col_temp = ''
    col_title = '"company_no",'
    for col in table.iloc[0]:  # 跑第1列

        if col_temp == '':  # 跑第一次
            for key, _ in table_name.items():
                # 先加公司company_no
                if not mssql.query_column_exist(cursor, key, 'company_no'):
                    mssql.alter_column(
                        cursor, key, 'company_no', 'nvarchar(60)', 'null')

        if col_temp == col:  # 累積2次+%
            col = col+"%"
        if col == list(table_name.values())[0]: #取第0筆的值
            for key, _ in table_name.items():
                if not mssql.query_column_exist(cursor, key,'type'):
                    mssql.alter_column(cursor, key, 'type',
                                       'nvarchar(60)', 'null')
        else:
            for key, _ in table_name.items():
                if not mssql.query_column_exist(cursor, key, col):
                    mssql.alter_column(
                        cursor, key, col, 'nvarchar(60)', 'null')

        col_temp = col
        if col == list(table_name.values())[0]:
            col_title = col_title+'"type",'
        else:
            col_title = col_title+'"'+col+'"'+','

    # 各表資料寫入
    balance_type = ''
    col_title = col_title[:-1]
    table_temp = ''
    row_count = len(table.index) - 1
    for x in range(row_count):
        col_detail = ''
        for col in table.iloc[x]:
            if col in table_name.values(): #insert尋找寫入時,對應的資料表 
               table_temp = list(table_name.keys())[list(table_name.values()).index(col)] 
               #value to key : list(取得列表all keys)[list(取得列表的所有值.index尋找在第幾個位置)]
               break
            else:
                col_detail = col_detail.replace("\xa0","")+"'"+col+"'"+','
        col_detail = col_detail[:-1]
        if col_detail != '':
            mssql.query_values_not_exist_insert(
                cursor, table_temp, col_title, "'"+title_no+"'," + col_detail)
    cursor.close()
    print(title+'-完成')
