# -*- coding: utf-8 -*-
import requests
import time, os
from bs4 import BeautifulSoup
os.chdir('/Users/BoHai/Desktop/get_psu_from_nbs/tmpfiles')

# 15��:
# http:/www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/

BURL = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/'

shead = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'}

# get province
def province(url):
    resession = requests.session()
    pcode = 0   #检测响应状态码
    while pcode != 200: #如果发送了一个失败请求（非200响应）
        try:
            r = resession.get(url,headers=shead,allow_redirects=True,timeout=60)
            pcode = r.status_code
        except:
            time.sleep(2) #函数推迟执行的秒数
    doc = BeautifulSoup(r.content,"lxml",from_encoding='gbk')
    info = doc.select('tr > td > a')  #BeautifulSoup的select方法，利用标签筛选元素，返回list();组合查找
    provname = []
    provurl = []
    for a in info:
        provname.append(a.children.next())
        provurl.append(a['href'])
    return provname, provurl

# get city county town
def pcct(url):
    resession = requests.session()
    pcode = 0
    while pcode != 200:
        try:
            r = resession.get(url,headers=shead,allow_redirects=True,timeout=60)
            pcode = r.status_code
        except:
            time.sleep(2)
    doc = BeautifulSoup(r.content,"html5lib",from_encoding='gbk')
    info = doc.select('tr > td > a')
    info_len =len(info)
    cityname = []
    cityurl = []
    for i in range(1,info_len,2):
        cityname.append(info[i].string)
        cityurl.append(info[i]['href'])
    return cityname, cityurl

# get community
def village(url):
    resession = requests.session()
    pcode = 0
    while pcode != 200:
        try:
            r = resession.get(url,headers=shead,allow_redirects=True,timeout=60)
            pcode = r.status_code
        except:
            time.sleep(2)
    doc = BeautifulSoup(r.content,"html5lib",from_encoding='gbk')
    table = doc.find("table", "villagetable")
    info = table.select('tr > td')
    info_len = len(info)
    vname = []
    vcode = []
    vtype = []
    for i in range(3,info_len,3):
        vcode.append(info[i].string)
    for i in range(4, info_len,3):
        vtype.append(info[i].string)
    for i in range(5, info_len,3):
        vname.append(info[i].string)
    return vcode, vname, vtype

# ====================================================
#   start
# ====================================================

# get province
purl = BURL + 'index.html'
provname, provurl = province(purl)
# write province data to file
fout = file('province.txt','w')
for a in zip(provname, provurl):
    fout.write(a[0].encode('utf8'))
    fout.write('\t')
    fout.write(a[1].encode('utf8'))
    fout.write('\n')
fout.close()

# get city
fout = file("city.txt", 'w')
c1url = []
for a in provurl:
    curl = BURL + a
    cname, cturl = pcct(curl)
    c1url = c1url + cturl
    for b in zip(cname,cturl):
        fout.write(b[0].encode('utf8'))
        fout.write('\t')
        fout.write(b[1].encode('utf8'))
        fout.write('\n')
fout.close()

# get county
fout = file("county.txt", 'w')
c2url = []
for a in c1url:
    if a != '44/4419.html' and a != '44/4420.html':
        curl = BURL + a
        cname, courl = pcct(curl)
        courl1 = [a[0:2] + '/' + tmp for tmp in courl]
        c2url = c2url + courl1
        for b in zip(cname,courl):
            fout.write(b[0].encode('utf8'))
            fout.write('\t')
            fout.write(b[1].encode('utf8'))
            fout.write('\n')
fout.close()

# get town
fout = file("town.txt", 'w')
t1url = []
for a in c2url:
    turl = BURL + a
    tname, tourl = pcct(turl)
    tourl1 = [a[0:6] + tmp for tmp in tourl]
    t1url = t1url + tourl1
    for b in zip(tname, tourl):
        fout.write(b[0].encode('utf8'))
        fout.write('\t')
        fout.write(b[1].encode('utf8'))
        fout.write('\n')
fout.close()

# village
fout = file("village.txt", 'w')
for a in t1url:
    vurl = BURL + a
    vcode, vname, vtype = village(vurl)
    for b in zip(vcode, vname, vtype):
        fout.write(b[0].encode('utf8'))
        fout.write('\t')
        fout.write(b[1].encode('utf8'))
        fout.write('\t')
        fout.write(b[2].encode('utf8'))
        fout.write('\n')
fout.close()

# get ��ݸ����ɽ��town, ��������û��county level ������
fout = file("dongzhong_town.txt", 'w')
t2url = []
for a in c1url:  # 44/4419.html
    if a == '44/4419.html' or a == '44/4420.html' :
        turl = BURL + a
        tname, tourl = pcct(turl) # 19/00/441900005.html
        tourl1 = [a[0:2] + '/' + tmp for tmp in tourl]
        t2url = t2url + tourl1
        for b in zip(tname, tourl):
            fout.write(b[0].encode('utf8'))
            fout.write('\t')
            fout.write(b[1].encode('utf8'))
            fout.write('\n')
fout.close()

# get ��ݸ����ɽ��village
fout = file("dongzhong_village.txt", 'w')
for a in t2url:
    vurl = BURL + a
    vcode, vname, vtype = village(vurl)
    for b in zip(vcode, vname, vtype):
        fout.write(b[0].encode('utf8'))
        fout.write('\t')
        fout.write(b[1].encode('utf8'))
        fout.write('\t')
        fout.write(b[2].encode('utf8'))
        fout.write('\n')
fout.close()
