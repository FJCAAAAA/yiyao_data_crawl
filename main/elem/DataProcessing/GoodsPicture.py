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
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent


class GetJddjPicture(object):
    def __init__(self):
        self.url_file = 'E:\爬虫项目\饿了么\json\elem_for_yaojisong_leimu.json'

    def get_picture(self,url):
        user_agent = random.choice(pcUserAgent)
        header = {
            # 'Host': 'image-star.elemecdn.com',
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1'
        }
        return get_picture(url, 0, header)

    def save_picture(self):
        fail_list = open('fail_list.txt', 'a', encoding='utf-8')
        with open(self.url_file, 'r', encoding='utf-8') as f:
            num = 0
            for line in f:
                num += 1
                if num < 6019:
                    continue
                print('第 {} 行 图片开始爬取'.format(num))
                url_dict = json.loads(line)
                upc = url_dict.get('69码')
                upc_s = 0
                pic_list = url_dict["商品图片"]
                if pic_list:
                    for n in pic_list:
                        if n:
                            try:
                                upc_s += 1
                                path = 'E:/爬虫项目/饿了么/picture/' + upc + '_' + str(upc_s) + '.jpg'
                                content = self.get_picture(n)
                                write_bytes(content, path)
                            except Exception:
                                print(traceback.format_exc())
                                fail_list.write(' '.join([str(num), n]) + '\n')
                                fail_list.flush()
                                continue


if __name__ == '__main__':
    GJP = GetJddjPicture()
    GJP.save_picture()
