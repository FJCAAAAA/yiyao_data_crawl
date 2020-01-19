#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : mingju.py
@Author: Fengjicheng
@Date  : 2019/12/5
@Desc  : 古诗词网名句下载
'''

import random
import traceback
import time
import json
from tqdm import tqdm
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.JsonToCsv import *

def get_one_page(url):
    pattern1 = re.compile('《.*?》')

    header = {
        'Host': 'so.gushiwen.org',
        'User-Agent': random.choice(pcUserAgent),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    soup = get_soup(url, 0, header)
    if soup:
        all_ctt = soup.find('div', class_='sons')
        ctt_list = all_ctt.find_all('div', class_='cont')
        ctt_dict = {'名句': '', '作者': '', '著作': ''}
        file = open('名句.json', 'a', encoding='utf-8')
        for mingju in ctt_list:
            mingju_list = mingju.find_all('a')
            mingju_ctt = mingju_list[0].get_text().strip()
            mingju_auth_name = mingju_list[1].get_text()
            mingju_auth = pattern1.sub('', mingju_auth_name).strip()
            mingju_name = pattern1.findall(mingju_auth_name)[0].strip()
            ctt_dict['名句'] = mingju_ctt
            ctt_dict['作者'] = mingju_auth
            ctt_dict['著作'] = mingju_name
            file.write(json.dumps(ctt_dict, ensure_ascii=False) + '\n')
            file.flush()



def get_all_page():
    for num in tqdm(range(1,101)):
        url = 'https://so.gushiwen.org/mingju/default.aspx?p=%s&c=&t='%(num)
        get_one_page(url)
        time.sleep(1)

# if __name__ == '__main__':
#     try:
#         get_all_page()
#     except Exception:
#         print(traceback.format_exc())

obj = Json_Csv('名句.csv')
obj.trans('名句.json')