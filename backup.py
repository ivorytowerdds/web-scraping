import requests
import json
import xlrd
import pandas as pd
dataframe2=pd.DataFrame()
wb = xlrd.open_workbook('smsjk.xlsx')
sh=wb.sheet_by_index(0)
rows=sh.nrows
for i in range(1,rows):
    cell_value = sh.cell(i,2).value
    if cell_value == '':
        pass
    else:
        url = 'http://ba.amac.org.cn/pages/amacWeb/user!list.action'
        data = {'filter_LIKES_CPMC': '',
        'filter_LIKES_GLJG': '',
        'filter_GES_SLRQ': '',
        'filter_LES_SLRQ': '',
        'filter_LIKES_CPBM': cell_value,
        'page.searchFileName': 'publicity_web',
        'page.sqlKey': 'PAGE_PUBLICITY_WEB',
        'page.sqlCKey': 'SIZE_PUBLICITY_WEB',
        '_search': 'false',
        'nd': '1512015344928',
        'page.pageSize': '50',
        'page.pageNo': '1',
        'page.orderBy': 'SLRQ',
        'page.order': 'desc'}
        
        header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Proxy-Connection': 'keep-alive',
        'Content-Length': '289',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Host': 'ba.amac.org.cn',
        'Origin': 'http://ba.amac.org.cn',
        'Referer': 'http://ba.amac.org.cn/pages/amacWeb/web-list.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
        
        
        req = requests.post(url, headers = header ,data = data)
        strtry = req.text
        count = len(strtry)
        if count > 400:
            #print(i)
            #req = requests.post(url, headers=header, data=data)
            jsonstr = json.loads(req.text)
            li = jsonstr.get('result')
            dataframe=pd.DataFrame(li,index=[i])
            dataframe2= pd.concat([dataframe2,dataframe],axis=0)
        else:
            pass

dataframe3=dataframe2.drop(['TZFW'],axis=1)
pd.DataFrame(dataframe3).to_csv('result.csv')