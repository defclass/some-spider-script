import requests
from lxml import etree
import codecs
import os

filename = '/home/hq/Desktop/raw-files/cat-url-uniq.txt'
dirname = "/home/hq/Desktop/raw-files/ContactPages/"

result=[]
i=0
with open(filename,'r') as f:
    for line in f:
        req = requests.get(line.replace("\n",""))
        if not os.path.isdir(dirname):
            os.makedirs(dirname )
        f = codecs.open(dirname+str(i)+".html", "w", "utf-8")
        f.write(req.text)
        f.close()
        i += 1

        
