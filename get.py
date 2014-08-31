#!/usr/bin/env python
import requests
import bs4
import re
#url = 'http://www.alibaba.com/products/F0/plastic_recycle/----------------------50----------------------------EU.html'
url = 'http://uk1019369980.trustpass.alibaba.com/contactinfo.html'

#将url转变为soup结构
def getSoup(url):
    response = requests.get(url)
    return bs4.BeautifulSoup(response.text,"html5lib")
    
#获取单个单面的所有url
def gSinglePageUrl(soup):
    title = soup.find_all("a",class_="cd dot-product",href=re.compile("contactinfo"))
    ## url的大数组
    urls = []
    for link in title:
        url = link.get('href')
        if  url not in urls:
            urls.append(url)
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
    
soup = getSoup(url);
getContactInfo(soup);
