#!/usr/bin/env python
import requests
import bs4
import re
from pyquery import PyQuery 
from lxml import etree
import urllib

url = 'http://www.alibaba.com/products/F0/plastic_recycle/----------------------50----------------------------EU.html'
url1 = 'http://uk1019369980.trustpass.alibaba.com/contactinfo.html'


#获取单个单面的所有url
def gSinglePageUrl(url):
    d = PyQuery(url=url)
    ## url的大数组
    urls = []
    d(".card .cat .atm").remove();
    d(".card .cat .dot-product").each(lambda:url = PyQuery(this).attr("href")  if url not in urls   urls.append()
                                      
    )
    return urls

#获取单个联系页面的信息    
def getContactInfo(soup):
    main_info = soup.select(".contact-detail .dl-horizontal")
    #反馈的信息数组
    info = {}
    key = 0
    for child in main_info[0].children:
        tag_text = child.string
        if not  tag_text.isspace():
            if key != 0:
                info[key] = re.sub('<[^>]+>','',tag_text)
                key = 0
                
            if bool(re.compile("Telephone").match(tag_text)):
                key = "Telephone"

            if re.compile("Mobile Phone").match(tag_text):
                key = "Mobile"
                
            if re.compile("Address").match(tag_text):
                key = "Address"
                
            if re.compile("Country/Region").match(tag_text):
                key = "Country/Region"

            if re.compile("City").match(tag_text):
                key = "City"

    return info;

print(gSinglePageUrl(url))
#getContactInfo(soup);
