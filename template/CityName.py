import requests
import os
from bs4 import BeautifulSoup


kujialeCityDir='F:\\kujialeCity\\'

url = 'https://www.kujiale.com/huxing/bj'

session = requests.session()
html = session.get(url)
soup = BeautifulSoup(html.text,'lxml')

#匹配带有class属性的li标签
taglist = soup.find_all('ul',attrs={'class':'province clearfix'})
for lilist in taglist:
    li=lilist.find_all('a',href=True)
    for da in li:
        href=da['href']
        if href.startswith('java'):
            os.makedirs(kujialeCityDir+da.string)
            kujialeSubCityDir=kujialeCityDir+da.string+'\\'
        else:
            kujialeSubCityPath=kujialeSubCityDir+da.string+'.txt'
            kujialeFile=open(kujialeSubCityPath,'w',encoding='utf-8')
            kujialeFile.write(href)
            kujialeFile.flush()
            print(href+da.string)




