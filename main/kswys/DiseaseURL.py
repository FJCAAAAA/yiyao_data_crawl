import requests
import random
from bs4 import BeautifulSoup
import main.kswys.UserAgent

def write_to_txt(dict):
    file = open(path,'a')
    file.write(dict['disease_url']+'\t'+dict['disease_name']+'\n')

path='disease.txt'
url="http://www.120ask.com/list/"
header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'__jsluid=18cd36d8cad4b417fc78b74acf6e8b54; comHealthCloudUserProfileUseTag=42643a921c6b45b6baa8c296ffdbf2ca; UM_distinctid=1696fd863fba0d-05479e111c796c-5e442e19-1fa400-1696fd863fc1be; Hm_lvt_7c2c4ab8a1436c0f67383fe9417819b7=1552359646; TUSHENGSID=TS1552359646560; _ga=GA1.2.628728754.1552359663; _gid=GA1.2.604886045.1552359663; page_keyword=%E5%8E%BB%E5%B9%B45%E6%9C%88%E5%8F%B3%E8%85%BF%E8%84%9A%E8%85%95%E9%9F%A7%E5%B8%A6%E6%8B%89%E4%BC%A4%E8%BF%87; CNZZDATA30036369=cnzz_eid%3D937902712-1552359625-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1552358799; Hm_lpvt_7c2c4ab8a1436c0f67383fe9417819b7=1552361637',
    'Host':'www.120ask.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':random.choice(main.kswys.UserAgent.pcUserAgent)
}
html=requests.get(url=url,headers=header)
soup = BeautifulSoup(html.text,'lxml')
tags=soup.find_all('p',attrs={'class':'clears'})
for tag in tags:
    lis=tag.findAll('a')
    for li in lis:
        dict={}
        disease_url=li['href']
        if disease_url.startswith('/list'):
            disease_url='http://www.120ask.com'+disease_url
        dict['disease_url']=disease_url
        disease_name=li.get_text()
        dict['disease_name']=disease_name
        write_to_txt(dict)
