#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ZhongYao_Detail.py.py
@Author: Fengjicheng
@Date  : 2019/9/17
@Desc  : 获取http://www.zhongyoo.com/name/ 网站下所有中药数据
'''

import requests
import random
import re
import traceback
import json
import time
from bs4 import BeautifulSoup
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.WebUtils import *
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

header = {
'Host': 'www.zhongyoo.com',
'User-Agent': random.choice(pcUserAgent),
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'close',
'Upgrade-Insecure-Requests': '1'
}
url_file = 'url_file.txt'

def get_all_url():
    file = open(url_file,'a',encoding='utf-8')
    for num in tqdm(range(1,46)):
        url = 'http://www.zhongyoo.com/name/page_%d.html' %(num)
        soup = get_soup(url,0,header)
        for n in soup.find_all('div',class_='sp'):
            page_url = n.strong.a.get('href')
            page_name = n.strong.a.get('title')
            file.write(page_name + ' ' + page_url + '\n')
            file.flush()
    file.close()
    print("所有中药链接已写入文件")


def get_all_page():
    # url = 'http://www.zhongyoo.com/name/zuiyucao_616.html'
    pattern1 = re.compile('【.*?】')
    pattern2 = re.compile('【|】')
    pattern3 = re.compile('\\s')
    with open(url_file,'r',encoding='utf-8') as f:
        url_list = f.readlines()
    for n in tqdm(url_list):
        url = re.split(' ',n)[1].strip()
        soup = get_soup(url, 0, header)
        soup_text = soup.find('div',class_='gaishu').find('div',class_='text')
        img = soup_text.find('img')
        text = soup_text.get_text()
        title_list = pattern1.findall(text)
        text_list = re.split(pattern1, text)
        text_list_new = [value.strip() for value in text_list if value.strip() != '\\s' and value.strip() != '']
        if len(title_list) == len(text_list_new):
            detail_dict = {}
            for n,m in zip(title_list,text_list_new):
                detail_dict[re.sub(pattern2,'',n)] = re.sub(pattern3,'',m)
            if img:
                detail_dict['图片'] = 'http://www.zhongyoo.com' + img.get('src')
            insert('zhongyao',detail_dict)
            time.sleep(3)
            # print(json.dumps(detail_dict,ensure_ascii=False))
        else:
            print("字段和内容数量不匹配",url)


if __name__ == '__main__':
    try:
        #get_all_url()
        get_all_page()
    except Exception:
        print(traceback.format_exc())