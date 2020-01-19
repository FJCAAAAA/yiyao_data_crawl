#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GoodsPicture.py.py
@Author: Fengjicheng
@Date  : 2019/9/25
@Desc  : 获取产品图片
'''

import random
import json
import traceback
from tqdm import tqdm
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent

class GetJddjPicture(object):
    def __init__(self):
        self.url_file = 'jddj.json'

    def get_jddj_picture(self,url):
        user_agent = random.choice(pcUserAgent)
        header = {
            'Host': 'img30.360buyimg.com',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
        return get_picture(url,0,header)


    def write_jddj_picture(self):
        with open(self.url_file,'r',encoding='utf-8') as f:
            for line in tqdm(f):
                url_dict = json.loads(line)
                oid = url_dict["_id"]["$oid"]
                oid_s = 0
                pic_list = url_dict["图片"]
                for n in pic_list:
                    #判断是否为图片
                    pic_kind = re.split('\.',n)[-1]
                    if pic_kind == 'jpg' or pic_kind == 'png':
                        oid_s = oid_s + 1
                        path = 'picture/' + oid + '_' + str(oid_s) + '.' + pic_kind
                        content = self.get_jddj_picture(n)
                        write_bytes(content, path)
                    else:
                        print('非图片格式',n)


if __name__ == '__main__':
    GJP = GetJddjPicture()
    try:
        GJP.write_jddj_picture()
    except Exception:
        print(traceback.format_exc())