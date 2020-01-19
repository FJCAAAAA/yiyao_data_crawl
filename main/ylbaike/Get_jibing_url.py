#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : geturl.py
@Author: Fengjicheng
@Date  : 2019/8/11
@Desc  :科学百科疾病症状分类,共7245个url，0-300页,每页24个，301页，21个，共302页
'''
import urllib.parse
import urllib.request
import json
from io import BytesIO
import gzip
import random
import yiyao_data_crawl.main.ylbaike.user_agent
import time


def get_url(page_num):
    agent = random.choice(yiyao_data_crawl.main.ylbaike.user_agent.user_agent_list)
    url = 'https://baike.baidu.com/wikitag/api/getlemmas'
    # header中原先加入了'Content-Length':91,导致手动post获取响应和页面不一致
    header = {
        'Host': 'baike.baidu.com',
        'User-Agent': agent,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://baike.baidu.com/wikitag/taglist?tagId=75953',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    data = {
        'limit': 24,
        'timeout': 3000,
        'filterTags': [],
        'tagId': 75953,
        'fromLemma': 'false',
        'contentLength': 40,
        'page': page_num
    }
    port_data = bytes(urllib.parse.urlencode(data),encoding='utf8')
    try:
        req = urllib.request.Request(url,headers=header,data=port_data)
        response = urllib.request.urlopen(req)
    except Exception as e:
        print('该次请求失败，继续下一次请求')
    content = response.read()
    code = response.getcode()
    buff = BytesIO(content)
    f = gzip.GzipFile(fileobj=buff)
    res = f.read().decode('utf-8')
    res_list = json.loads(res)['lemmaList']
    with open('jibing_url.txt', 'a',encoding='gbk') as n:
        for res_dict in res_list:
            n.write (str({res_dict['lemmaTitle']:res_dict['lemmaUrl']})+'\n')
    #      print(str({res_dict['lemmaTitle']:res_dict['lemmaUrl']}))


def get_all_url():
    for i in range(302):
        try:
            get_url(i)
            print("第",i,"页","写入文件成功。")
        except Exception as e:
            print("第",i,"页","写入文件失败！")
        time.sleep(2)

if __name__ == "__main__":
    get_all_url()