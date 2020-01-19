#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : SearchDis.py
@Author: Fengjicheng
@Date  : 2019/12/31
@Desc  : 寻医问药 搜索疾病 统计返回条目
'''
import random
import re
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.WebUtils import *


class Xunyiwenyao(object):
    def __init__(self):
        self.api = 'http://so.xywy.com/comse.php'
        self.api_1 = 'http://so.xywy.com/comse.php?keyword=%E6%84%9F%E5%86%92&page=1&src=so'

    def search(self, keyword, page):
        data = {
            'keyword': keyword,
            'page': str(page),
            'src': 'so'
        }
        header = {
            'Host': 'so.xywy.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Referer': 'http://so.xywy.com/comse.php',
            'Upgrade-Insecure-Requests': '1'
        }
        soup = get_soup(self.api, 0, header, data)
        result = soup.find_all('a', class_='comse-result')
        if page == 1:
            pattern1 = re.compile('.*&page=(.*?)&src=so')
            page_last = soup.find('a', onmousedown="__svcl(this, 't=pageChange&p=9&w=尾页')").get('href')
            page_num_list = pattern1.findall(page_last)
            if len(page_num_list) == 1:
                page_num = page_num_list[0]
            else:
                page_num = '50'
            return [len(result), page_num]
        else:
            return [len(result)]

    # @staticmethod
    def get_all_page(self, keyword):
        page_num = int(self.search(keyword, 1)[1])
        result_len = 0
        for num in range(1, page_num+1):
            print('开始查找 {} 的 第 {} 页'.format(keyword, num))
            result_len += self.search(keyword, num)[0]
        return result_len


if __name__ == '__main__':
    obj = Xunyiwenyao()
    result_len = obj.get_all_page('咳嗽')
    print(result_len)

