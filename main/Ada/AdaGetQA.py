#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AdaGetQA.py
@Author: Fengjicheng
@Date  : 2019/11/25
@Desc  : 获取Ada app对话信息--request函数
'''

import requests
import urllib3
import redis
import random
import time
from yiyao_data_crawl.main.common.UserAgent import phoneUserAgent


class Ada(object):
    def __init__(self):
        self.cookie = 'route=eb82710af4986dfb3cd014ba19db11ab189995ac'
        #连接redis
        self.pool = redis.ConnectionPool(decode_responses=True)
        self.r = redis.Redis(connection_pool=self.pool)


    def get_one_qa(self, data):
        ada_token = ' '.join(['Bearer',self.r.get('ada_token')])
        header = {
            'accept': 'application/json',
            'authorization': ada_token,
            # 'user-agent': 'ada-api-js',
            'user-agent': random.choice(phoneUserAgent),
            'x-ada-platform': 'android',
            'x-ada-app-version': '2.49.3',
            'Content-Type': 'application/json;charset=utf-8',
            # 'Content - Length': '316',
            'Host': 'prod-mh-26.adahealth.net',
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept-Encoding': 'gzip',
            'Cookie': self.cookie
        }
        url = 'https://prod-mh-26.adahealth.net/api/ada/dialog'
        num = 0
        while True:
            num += 1
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(url, data=data, headers=header, timeout=(20, 20), verify=False)
            if num > 5:
                break
            if response:
                print('%s请求成功'%(url))
                break
            else:
                print('请求失败%s，1秒后再次请求'%(url))
                print(response.content.decode('utf-8'))
                time.sleep(1)
        # time.sleep(1)
        return response.content.decode('utf-8')


    def get_report(self, adaCaseKey):
        ada_token = ' '.join(['Bearer', self.r.get('ada_token')])
        header = {
            'accept': 'application/json',
            'authorization': ada_token,
            # 'user-agent': 'ada-api-js',
            'user-agent': random.choice(phoneUserAgent),
            'x-ada-platform': 'android',
            'x-ada-app-version': '2.49.3',
            'content-type': 'application/json;charset=utf-8',
            # 'Content - Length': '316',
            'Host': 'prod-mh-26.adahealth.net',
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept-Encoding': 'gzip',
            'Cookie': self.cookie
        }
        url = 'https://prod-mh-26.adahealth.net/api/ada/result/%s' %(adaCaseKey)
        while True:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=header, timeout=(20, 20), verify=False)
            if response:
                print('报告下载成功')
                break
            else:
                print('报告下载失败，1秒后再次请求')
                time.sleep(1)
        # time.sleep(1)
        return response.content.decode('utf-8')


    def get_profiles(self):
        ada_token = ' '.join(['Bearer', self.r.get('ada_token')])
        header = {
            'accept': 'application/json',
            'authorization': ada_token,
            # 'user-agent': 'ada-api-js',
            'user-agent': random.choice(phoneUserAgent),
            'x-ada-platform': 'android',
            'x-ada-app-version': '2.49.3',
            'content-type': 'application/json;charset=utf-8',
            # 'Content - Length': '316',
            'Host': 'prod-mh-26.adahealth.net',
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept-Encoding': 'gzip',
            'Cookie': self.cookie
        }
        url = 'https://prod-mh-26.adahealth.net/api/ada/profiles'
        while True:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=header, timeout=(20, 20), verify=False)
            if response:
                print('个人信息下载成功')
                break
            else:
                print('个人信息下载失败，1秒后再次请求')
                time.sleep(1)
        # time.sleep(1)
        return response.content.decode('utf-8')

    def get_ada_sym(self, sym):
        ada_token = ' '.join(['Bearer', self.r.get('ada_token')])
        header = {
            'accept': 'application/json',
            'authorization': ada_token,
            # 'user-agent': 'ada-api-js',
            'user-agent': random.choice(phoneUserAgent),
            'x-ada-platform': 'android',
            'x-ada-app-version': '2.49.3',
            'content-type': 'application/json;charset=utf-8',
            # 'Content - Length': '316',
            'Host': 'prod-ada-bff.adahealth.net',
            # 'Connection': 'Keep-Alive',
            'Connection': 'close',
            'Accept-Encoding': 'gzip',
            'Cookie': self.cookie
        }
        url = 'https://prod-ada-bff.adahealth.net/api/v1/symptoms?limit=20&query=%s&sex=MALE&birthday=1991-12-31' % (sym)
        while True:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.get(url, headers=header, timeout=(20, 20), verify=False)
            if response:
                break
            else:
                print('Ada症状名称查询失败，1秒后再次查询')
                time.sleep(1)
        # time.sleep(1)
        return response.content.decode('utf-8')