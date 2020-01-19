import requests
import os
from bs4 import BeautifulSoup


anjukeCityDir='F:\\kujialeCity\\'

url = 'https://www.anjuke.com/sy-city.html'

session = requests.session()
html = session.get(url)
soup = BeautifulSoup(html.text,'lxml')

#匹配带有class属性的li标签
taglist = soup.find_all('div',attrs={'class':'city_list'})
for lilist in taglist:
    li=lilist.find_all('a',href=True)
    for da in li:
        print(da.string)
        href=da['href']
        # print(href)
        anjukeCityPath=anjukeCityDir+da.string+'.txt'
        anjukeFile=open(anjukeCityPath,'w',encoding='utf-8')
        anjukeFile.write(href)
        anjukeFile.flush()
        print(href+da.string)




