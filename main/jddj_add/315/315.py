#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : 315.py
@Author: Fengjicheng
@Date  : 2019/10/22
@Desc  :
'''

import re
import time
import random
import traceback
from tqdm import tqdm
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

class Get315Detail(object):
    def __init__(self):
        self.ChengyaoUrl='https://www.315jiage.cn/ChengYao/'
        self.ChengyaoPage = 4073
        self.XiyaoUrl = 'https://www.315jiage.cn/XiYao/'
        self.XiyaoPage = 3654
        self.header = {'Host': 'www.315jiage.cn','User-Agent': random.choice(pcUserAgent),
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Referer': 'https://www.315jiage.cn/ChengYao/defaultp2.htm',
                       'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                       'Connection': 'close'}

    def GetAllUrl(self,url,page,filename):
        pattern1 = '\.\.'
        file = open(filename,'a',encoding='utf-8')
        for n in tqdm(range(1,page+1)):
            if n == 1:
                PageUrl = ''.join([url,'default.htm'])
            else:
                PageUrl = ''.join([url,'defaultp',str(n),'.htm'])
            soup = get_soup(PageUrl,0,self.header)
            ScardList = soup.find('div',class_='mm sCard-list')
            for n in ScardList.find_all('div',class_='sCard'):
                TitleText = n.find('div', class_='title text-oneline')
                MedUrl = 'https://www.315jiage.cn' + re.sub(pattern1,'',TitleText.a.get('href'))
                MedName = TitleText.a.get_text()
                file.write(' '.join([MedUrl,MedName,'\n']))
                file.flush()
        file.close()

    def GetOnePage(self,url):
        pattern1 = re.compile('产品名称：[^\\s]+|规格：[^\\s]+|剂型：[^\\s]+|包装单位：[^\\s]+|批准文号：[^\\s]+|生产厂家：[^\\s]+|条形码：[^\\s]+')
        pattern2 = re.compile('：')
        soup = get_soup(url,0,self.header)
        content = soup.find('div',id='content')
        ContentDict = {}
        for n in content.find_all('p'):
            ContentP = n.get_text().strip()
            ContentPIndex = pattern1.findall(ContentP)
            if ContentPIndex:
                for m in ContentPIndex:
                    ContentList = re.split(pattern2,m)
                    ContentDict[ContentList[0]] = ContentList[1]
        return ContentDict

    def GetAllPage(self,filename):
        with open(filename,'r',encoding='utf-8') as f:
            AllUrlList = f.readlines()
        file = open('fail.txt','a',encoding='utf-8')
        for n in tqdm(AllUrlList):
            UrlList = re.split(' ',n.strip())
            Medurl = UrlList[0]
            MedName = ''.join(UrlList[1:])
            try:
                ContenDict = self.GetOnePage(Medurl)
                ContenDict['原始名称'] = MedName
                insert('ypjg315',ContenDict)
                # print(ContenDict)
            except Exception:
                print('%s,%s爬取失败'%(Medurl,MedName))
                print(traceback.format_exc())
                file.write(' '.join([Medurl,MedName,'\n']))
                continue


if __name__ == '__main__':
    obj = Get315Detail()
    # #获取成药url
    # obj.GetAllUrl(obj.ChengyaoUrl,obj.ChengyaoPage,'chengyao.txt')
    # #获取西药url
    # obj.GetAllUrl(obj.XiyaoUrl,obj.XiyaoPage,'xiyao.txt')
    # #获取成药详情
    # obj.GetAllPage('chengyao.txt')
    # #获取西药详情
    # obj.GetAllPage('xiyao.txt')

