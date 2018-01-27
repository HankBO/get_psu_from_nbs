# -*- coding: utf-8 -*-
import requests
import os
import urllib
from bs4 import BeautifulSoup
import pandas as pd

sdata = pd.read_stata(os.path.abspath('/Users/BoHai/Desktop/get_psu_from_nbs/tmpfiles/post_need.dta'), encoding='utf8')
sdata['postcode'] = u''
num = sdata.shape[0]

shead = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'}

for i in range(num):
    try:
        r = requests.session()
        r.headers = shead
        addstr = sdata.pstr[i].encode('gbk')
        add_url = urllib.quote(addstr)
        r0 = r.get('http://opendata.baidu.com/post/s?wd=' + add_url)
        doc0 = BeautifulSoup(r0.content, 'html5lib', from_encoding="gbk")
        t1 = doc0.find('ul')
        t2 = t1.li.a
        postcode = t2.get_text()
    except:
        postcode = u''
    sdata.postcode[i] = postcode
sdata.to_excel(os.path.abspath('/Users/BoHai/Desktop/get_psu_from_nbs/outfiles/post_python.xlsx'), index=False)
