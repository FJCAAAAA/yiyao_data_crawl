#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetJingyaotong.py
@Author: Fengjicheng
@Date  : 2020/1/3
@Desc  : 京药通App 药品数据采集
'''
import requests
import time
import traceback
from yiyao_data_crawl.main.common.GetMD5 import get_md5


class RequestJingYaoTong(object):
    def __init__(self):
        self.api_cate = 'http://ydapi.yjj.beijing.gov.cn/basicinfo/sbasicInfoAction!comboxTreeByParam.do?paramValue=YPYTFL'
        self.api_med_list = 'http://ydapi.yjj.beijing.gov.cn/storedrugrel/storedrugrelRefAction!searchDrugList.do?'
        self.api_med_detail = 'http://ydapi.yjj.beijing.gov.cn/storedrugrel/storedrugrelRefAction!getDrugInfoById.do?'
        self.api_picture = 'http://ydapi.yjj.beijing.gov.cn/static/'
        self.header = {
            'Host': 'ydapi.yjj.beijing.gov.cn',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.4.1',
            'Connection': 'keep-alive'
        }
        self.header_pic = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; OPPO R11 Build/NMF26X)',
            'Host': 'ydapi.yjj.beijing.gov.cn',
            'Accept-Encoding': 'gzip',
            'Connection': 'close'
        }

    def get_sign(self, params):
        secret = 'hxsecret2019'
        return get_md5(params + secret)

    def for_request(self, request):
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

    def get_med_cate(self):
        '''
        药品类目request函数
        :return: 
        '''
        response = self.for_request(requests.get(self.api_cate, headers=self.header, timeout=(10, 10)))
        if response:
            return response.content.decode('utf-8')

    def get_med_list(self, drugType, pageIndex):
        '''
        药品类目下药品列表request函数
        :param drugType: 药品类目
        :param pageIndex: 页数
        :return: 
        '''
        timestamp = str(round(time.time() * 1000))
        params = 'appKey=hxkey2019&drugType={}&pageIndex={}&pageSize=10&timestamp={}'.format(drugType, pageIndex, timestamp)
        sign = self.get_sign(params)
        params_full = 'appKey=hxkey2019&searchKey=&drugType={}&pageIndex={}&pageSize=10&timestamp={}&sign={}'.format(drugType, pageIndex, timestamp, sign)
        url = self.api_med_list + params_full
        response = self.for_request(requests.get(url, headers=self.header, timeout=(10, 10)))
        if response:
            return response.content.decode('utf-8')
        # return url

    def get_med_detail(self, drugId):
        '''
        药品详情request函数
        :param drugId: 药品id
        :return: 
        '''
        timestamp = str(round(time.time() * 1000))
        params = 'appKey=hxkey2019&drugId={}&latitude=39.791684&longitude=116.570066&timestamp={}'.format(drugId, timestamp)
        sign = self.get_sign(params)
        params_full = 'appKey=hxkey2019&longitude=116.570066&latitude=39.791684&drugId={}&userId=&storeId=&timestamp={}&sign={}'.format(drugId, timestamp, sign)
        url = self.api_med_detail + params_full
        response = self.for_request(requests.get(url, headers=self.header, timeout=(10, 10)))
        if response:
            return response.content.decode('utf-8')

    def get_picture(self, route):
        '''
        药品图片request函数
        :param route: 
        :return: 
        '''
        url = self.api_picture + route
        response = self.for_request(requests.get(url, headers=self.header_pic, timeout=(10, 10)))
        return response.content




if __name__ == '__main__':
    obj = RequestJingYaoTong()
    print(obj.get_med_list('01', '31'))
    # print(obj.get_med_detail('7456572cc3e111e99d48801844edb918'))
    # print(obj.get_med_cate())
