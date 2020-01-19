#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : config.py
@Author: Fengjicheng
@Date  : 2019/12/25
@Desc  : 配置
'''
import random
import traceback
from yiyao_data_crawl.main.common.UserAgent import phoneUserAgent


def get_header():
    header = {
        'Host': 'newretail.ele.me',
        'User-Agent': random.choice(phoneUserAgent),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
    }
    return header


def for_request(request):
    request_num = 0
    while True:
        request_num += 1
        if request_num > 5:
            return False
        else:
            try:
                return request
            except Exception:
                print(traceback.format_exc())
                continue