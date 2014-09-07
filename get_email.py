#!/usr/bin/env python
import os,urllib, datetime,random, time
from sys import argv
import bs4
import re
import requests
import errno

user_agents = list()
csv_file = "/home/hq/Desktop/source.cvs"
avail_info = "/home/hq/Desktop/avail_info.cvs"
bad_info = "/home/hq/Desktop/bad_info.cvs"
company_names = []
company_websites = []

def main():
    company_info = readSourceFile(csv_file)
    # 抓取失败的公司列表
    failed_info = []
    for k,i in enumerate(company_info):
            print(k)
            if isInList(i):
                continue
            addList(i)
            print("创建google链接")
            # 创建google 链接
            url = createGoogleUrl(i[0],i[1])
            print("获取google页面: " + url)
            # 获取搜索页面内容
            content = getContent(url)
            if not  content:
                continue
        
            # 分析所有的有用url
            urls = pregAllUrls(content)
            print("正在获取搜索页内的" + str(len(urls)) +"个url")
            # 收集所有页面并提取email
            str_all = getAllContent(urls)
            
            emails = pregEmails(str_all)
            #去重,排序,收集两个email
            avail_emails  = getLessTwoEmail(scoreSort(scoreEmail(i[1],set(emails))))
            email_field = buildEmailField(avail_emails)
            i[7] = email_field
            if email_field:
                success_write(",".join(i))
            else:
                failed_info.append(",".join(i))
                fails_write(",".join(i))
                
                
            print("可用的Email为：" + email_field)
            print("\n\n")
            print("下一个链接开始...")
            

# 成功的email 依次写入到成功的文件中
def success_write(str):
    try:
        f=open(avail_info,'a')
        f.write(str)
        f.write('\n')
        f.close()
    except:
        print("写入avail_info文件失败:" + str)
    
# 失败的email 一次性写入到失败的文件中
def fails_write(str):
    try:
        f=open(bad_info,'a')
        f.write(str)
        f.write('\n')
        f.close()
    except:
        print("写入bad_info文件失败")
    
# 判断该公司是否在列表中            
def isInList(info):
    if info[0].lower() in company_names:
        return 1

    if (not info[1]) and info[1].lower() in company_websites:
        return 1

    return 0

# 将已经处理的公司加到列表中
def addList(info):
    company_names.append(info[0].lower())
    company_websites.append(info[1].lower())
    
# 把所有url字符串全拉下来组成一个大字符串
def getAllContent(urls):
    # 收集所有页面
    str_coll = ''
    for j in urls:
        print("收集 " + j + " 中的页面代码")
        content = getContent(j)
        if not  content:
            continue
            
        str_coll += content
    return str_coll


            
# 构造email字段    
def buildEmailField(emails):
    email = ""
    for e in emails:
        email = email + e.get("email") + "; "

    return email
    
            
# @return 0 or 1 
def validateEmail(email):
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
        return 1
            
    return 0

# @var url http://www.germanplast.com
# @return "germanplast.com"
def getDomain(url):
    url = url.lower()
    
    if not re.match(r'^https?:/{2}\w.+$', url):
        return "None Domain"
        
    p = urllib.parse.urlparse(url)
    # 阿里的网址
    if re.match(r'.*alibaba.*',p.netloc) :
        return "None Domain"
    # 带www的
    elif re.match(r'www\.(.*)',p.netloc):
        return p.netloc.replace('www.',"")
    else:
        return p.netloc
        
# @var email 如abc@qq.com
# @return  ["abc", "qq"]
def getEmailInfo(email):
    if not validateEmail(email):
        #raise Exception('getEmailInfo(): '+ email + '不是有效的email地址');
        return ["none","none"]
        
    username,host = email.split('@')
    domain_scrap,state = host.split('.')
    return [username,domain_scrap]

def getTrustLevel(score):
    if(score == 0):
        return "normal"
    elif(score == 1):
        return "some relative"
    elif(score ==11):
        return "that's it"
        
        
# 根据url 将email相关性评分
def scoreEmail(url, emails):
    names = ["info","sales","webmaster", "trade"]
    domain_name = getDomain(url)
    domain_scrap = domain_name.split('.')
    userful_domain_scrap = domain_scrap[0];
    chosen_emails = []
    for e in emails:
        score = 0
        email_user, email_domain_scrap = getEmailInfo(e)
        if email_user in names :
            score += 1
            
        if email_domain_scrap == userful_domain_scrap :
            score += 10
            
        single_email = {'email':e,'score':score}
        chosen_emails.append(single_email)
        
    return chosen_emails

# 根据email的相关性进行排序
# 返回 [{'email': 'info@ereciklaza.com', 'score': 11}, {'email': 'info@qq.com', 'score': 1}, {'email': 'abc@bcd.com', 'score': 0}]
def scoreSort(emails):
    for passnum in range(len(emails)-1,0,-1):  
        #print emails,passnum  
        for i in range(passnum):
            if emails[i].get('score') < emails[i+1].get('score'):  
                temp = emails[i]  
                emails[i] = emails[i+1]  
                emails[i+1] = temp

    return emails  

# 查找字符串中所有的email，以数组返回
def pregEmails(content):
    mailre = re.compile(r"(\w+@[a-zA-Z0-9-_]+\.\w+)")
    return mailre.findall(content)

def load_user_agent():
    fp = open('./user_agents', 'r')

    line  = fp.readline().strip('\n')
    while(line):
        user_agents.append(line)
        line = fp.readline()
    fp.close()


# 返回两个email就可以了
def getLessTwoEmail(emails):
    if len(emails) > 2:
        return [emails[0], emails[1]]
    else :
        return emails;

        
def randomSleep():
    sleeptime =  random.randint(10, 16)
    time.sleep(sleeptime)

# 抓取网页内容,返加字符串
def getContent(url):
    # Load use agent string from file
    load_user_agent()
    length = len(user_agents)
    index = random.randint(0, length-1)
    user_agent = user_agents[index]
    headers = {'User-Agent': user_agent}
    # 谷歌的链接就休息一下
    if re.match(r"google",url):
        randomSleep()
        
    try:
        response = requests.get(url, headers = headers,timeout=30)
        if response.status_code ==  requests.codes.ok :
            return response.text
        else:
            return 0
            
    except:
        print("网络连接错误")
        
def pregAllUrls(content):
    urls = []
    soup = bs4.BeautifulSoup(content)
    for a in soup.select(".r a"):
        href = a.attrs.get('href')
        urlre = re.compile(r"(/url\?q=)")
        if urlre.findall(href):
            b = href.split("/url?q=")
            c = b[1].split('&')
            urls.append(urllib.parse.unquote(c[0]))
    return urls

# 根据url 和公司名字 生成正确的搜索网址
def createGoogleUrl(company_name, url):
    company_name = company_name.lower()
    url = url.lower()
    base_url = "https://www.google.com.hk/search?hl=en&q="
    # 如果不存在
    if not url :
        return base_url + company_name + " email"

    if  re.search("alibaba", url) :
        return base_url + company_name + " email"
    elif re.search("http://", url) :
        return base_url  + "email " +  url
    else :
        return base_url + company_name + " email"
        exit()
        

def readSourceFile(path):
    company_info = []
    for line in open(path):
        a = line.replace('\n','').split(",")
        company_info.append(a)

    return company_info
        
main()        

