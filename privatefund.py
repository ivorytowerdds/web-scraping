# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:50:50 2017

@author: cys
"""

import requests
from collections import OrderedDict
import pandas as pd
import re
import threading
from bs4 import BeautifulSoup as bs

def get_size(size):
    html_url='http://gs.amac.org.cn/amac-infodisc/api/fund/account?rand=0.7588787459931894&page=0&size={}'.format(size)
    headers={
            u'Accept':u'application/json, text/javascript, */*; q=0.01',
            u'Accept-Encoding':u'gzip, deflate',
            u'Accept-Language':u'zh-CN,zh;q=0.9',
            u'Content-Length':u'2',
            u'Content-Type':u'application/json',
            u'Host':u'gs.amac.org.cn',
            u'Origin':u'http://gs.amac.org.cn',
            u'Proxy-Connection':u'keep-alive',
            u'Referer':u'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
            u'User-Agent':u'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            u'X-Requested-With':u'XMLHttpRequest'
            } 
    payload='{"type":"一对多"}'.encode('utf-8')
    res=requests.post(html_url,headers=headers,data=payload)
    content=res.json()
    return content

size=get_size(1)['totalElements'] #get the size

yddid=[]
def get_id(size):
    html_url='http://gs.amac.org.cn/amac-infodisc/api/fund/account?rand=0.7588787459931894&page=0&size={}'.format(size)
    headers={
            u'Accept':u'application/json, text/javascript, */*; q=0.01',
            u'Accept-Encoding':u'gzip, deflate',
            u'Accept-Language':u'zh-CN,zh;q=0.9',
            u'Content-Length':u'2',
            u'Content-Type':u'application/json',
            u'Host':u'gs.amac.org.cn',
            u'Origin':u'http://gs.amac.org.cn',
            u'Proxy-Connection':u'keep-alive',
            u'Referer':u'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
            u'User-Agent':u'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',
            u'X-Requested-With':u'XMLHttpRequest'
            }
    payload='{"type":"一对多"}'.encode('utf-8')
    res=requests.post(html_url,headers=headers,data=payload)
    content=res.json()
    
    for i in range(size):
        yddid.append(content['content'][i]['id'])
    return yddid
yddid=get_id(size)

url_list = []
for k in yddid:
    url_list.append('http://gs.amac.org.cn/amac-infodisc/res/fund/account/{}.html'.format(k))

#url='http://gs.amac.org.cn/amac-infodisc/res/fund/account/91990a40-a016-4313-920c-d84c8ced2a27.html'

dict1=OrderedDict()
dict1['基金ID']=[i for i in yddid]

result_content=[]
result_title=[]
def get_title(url):
    # url = url_list[0]
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Host':'gs.amac.org.cn',
        #'If-Modified-Since':'Sun, 19 Nov 2017 16:34:54 GMT',
        #'If-None-Match':'W/"5a11b2ae-204c"',
        'Proxy-Connection':'keep-alive',
        'Referer':'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    soup = bs(res.text, 'lxml')
    tag_a = soup.find_all(attrs={'class':'table table-center table-info'})[0].find_all('td',attrs={'class':'td-title'})
    for item in tag_a:
        result_title.append(item.string)
    return result_title

result_title=get_title(url_list[0])
result_title.pop()

def tool(s):
    s=re.sub(u'\n',u'',s)
    s=re.sub(u'<.*?>',u'',s)
    s=re.sub(u' ',u'',s)
    s=re.sub(u'\t',u'',s)
    s=re.sub(u'\r',u'',s)
    return s     
   
def get_detail(url):
    # url = url_list[0]
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cache-Control':'max-age=0',
        'Host':'gs.amac.org.cn',
        #'If-Modified-Since':'Sun, 19 Nov 2017 16:34:54 GMT',
        #'If-None-Match':'W/"5a11b2ae-204c"',
        'Proxy-Connection':'keep-alive',
        'Referer':'http://gs.amac.org.cn/amac-infodisc/res/fund/account/index.html',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
        }
    try:
        res = requests.get(url,headers=headers)
        res.encoding = 'utf-8'
        soup = bs(res.text, 'lxml')
        content_a=soup.find_all(attrs={'class':'table table-center table-info'})[0].find_all('td',attrs={'class':'td-content'})
        result_content.append([tool(content_a[i].string) for i in range(0,len(content_a)-1)])
    except:
        print('miss page: ', url)
    return result_content

def threading_process(get_detail, url_list) :      
    thread = []      
    for i in url_list:
        # print(i)
        spin = threading.Thread(target=get_detail, args=(i,))
        thread.append(spin)
    for i in range(len(thread)):
        thread[i].start()
    for i in range(len(thread)):
        thread[i].join() 

threading_process(get_detail, url_list)

for i in range(len(result_title)):
    dict1[result_title[i]]=[result_content[j][i] for j in range(size)]
pd.DataFrame(dict1).to_csv('pf.csv')      

