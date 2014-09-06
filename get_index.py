#!/usr/bin/env python
import requests
from lxml import etree
import codecs
import os

#定义变量
url1 = 'http://www.alibaba.com/products/F0/plastic_recycle/----------------------50----------------------------EU'
url2 = ".html"

dirname = "/home/hq/Desktop/raw-files/indexPages/"


if not os.path.isdir(dirname):
    os.makedirs(dirname )

i=0
while(1):
    if i == 0:
        url = url1 + url2
    if i > 40:
        break
    else:
        url = url1 + "/" + str(i) + url2
    req = requests.get(url)
    if req.status_code == 200 :
        f = codecs.open(dirname+str(i)+".html", "w", "utf-8")
        f.write(req.text)
        f.close()
    i += 1
