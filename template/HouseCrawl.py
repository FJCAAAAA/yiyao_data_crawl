# coding:utf-8

import requests
import re
import time
import os
import main.python.fjn.Proxies
from bs4 import BeautifulSoup

def get_quyu_url(url):
    list=[]
    req=requests.get(url=url,headers=headers,proxies=main.python.fjn.Proxies.proxies)
    html=req.text
    soup = BeautifulSoup(html,'lxml')
    til=soup.find_all('div',attrs={'class':'items'})
    for ti in til:
        t=ti.find_all('a',attrs={'title':re.compile('.*')})
        for xt in t:
            title_name=xt['title']
            if title_name=='全部小区':
                continue
            else:
                if title_name.endswith('周边小区'):
                    break
                else:
                    print(title_name)
                    href=xt['href']
                    print(href)
                    list.append(href)
    return list

def get_house_num(url):
    req=requests.get(url=url,headers=headers,proxies=main.python.fjn.Proxies.proxies)
    html=req.text
    soup = BeautifulSoup(html,'lxml')
    title=soup.find_all('div',attrs={'class':'sortby'})
    for til in title:
        num=til.find('span',attrs={'class':'tit'})
        # print(num)
        count=0
        for nu in num:
            count=count+1
            if count==4:
                s=str(nu)
                shu_liang=s[4:(s.find('/')-1)]
                print(shu_liang)
                return shu_liang

def get_house_page(shu_liang):
    if int(shu_liang)>3000:
        pages=105
    else:
        pages=int(int(shu_liang)//30)+5
    return pages

def write_to_file(house_name):
    file = open(path,'a')
    file.write(house_name+'\n')


def get_house_name(url):
    req=requests.get(url=url,headers=headers,proxies=main.python.fjn.Proxies.proxies)
    html=req.text
    soup = BeautifulSoup(html,'lxml')
    taglist = soup.find_all('div',attrs={'class':'li-itemmod'})
    for lilist in taglist:
        al=lilist.find_all('img')
        for a in al:
            house_name=a['alt']
            write_to_file(house_name)


city_name='tianjin'
cityDir='F:\\anjuke\\'+city_name+'\\'
if not os.path.exists(cityDir):
    os.makedirs(cityDir)
father_url='https://'+city_name+'.anjuke.com/community/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
quyu_urls=get_quyu_url(father_url)
for quyu_url in quyu_urls:
    shu_liang=get_house_num(quyu_url)
    quyu_name=quyu_url[8+len(city_name)+22:-1]
    pages=get_house_page(shu_liang)
    print(pages)
    path=cityDir+quyu_name+'.txt'
    for page in range(1,pages):
        time.sleep(2)
        url=quyu_url+'/p'+str(page)+'/'
        get_house_name(url)
# get_quyu_name('https://'+city_name+'.anjuke.com/community/'+quyu_name+'/p'+str(pages)+'/')
# get_house_num('https://'+city_name+'.anjuke.com/community/'+quyu_name+'/p'+str(pages)+'/')