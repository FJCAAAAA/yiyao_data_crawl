#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_LngLat_Tengxun.py
@Author: Fengjicheng
@Date  : 2019/10/28
@Desc  : 通过腾讯地图API获取指定地点经纬度
'''

import requests
import traceback
import time


class GetLngLatTengxun(object):
    def __init__(self):
        self.api = 'https://apis.map.qq.com/ws/geocoder/v1/'
        self.api_search = 'https://apis.map.qq.com/ws/place/v1/search'
        self.api_reverse = 'https://apis.map.qq.com/ws/geocoder/v1/'
        self.key =''

    def LngLat(self,address):
        '''
        通过腾讯地图API获取指定地址经纬度--地址解析接口
        :param address: 具体地址
        :return: json
        '''
        params = {'address': address, 'key': self.key}
        try:
            res = requests.get(self.api, params, timeout=10)
            time.sleep(1)
            return res.json()
        except Exception:
            print(traceback.format_exc())

    def LngLatBySearch(self, district, size, keyword, times):
        '''
        通过腾讯地图API获取指定地址经纬度--地点搜索接口，默认取第一个，准确率相对于“地址解析接口”较高
        :param district: 城市名称
        :param size: 返回第几页，默认第一页
        :param keyword: 地点名称
        :param times: 
        :return: lat,lng
        '''
        if times > 9:
            return 0
        times = times + 1
        params = {
            'boundary': 'region({},0)'.format(district),
            'page_size': '20',
            'page_index': str(size),
            'keyword': keyword,
            'orderby': '_distance',
            'key': self.key
        }
        try:
            response = requests.get(self.api_search, params, timeout=10)
            time.sleep(1)
        except Exception as e:
            return self.retry(district, size, keyword, times, '%s,try again'%(e))
        content = response.json()
        if content['status'] == 0:
            districts_list = content['data']
            if districts_list:
                districts_dict = districts_list[0]
                districts_geo_dict = districts_dict.get('location')
                districts_geo_str = '{},{}'.format(districts_geo_dict.get('lat'),districts_geo_dict.get('lng'))
                return districts_geo_str
            else:
                return ''
        else:
            print('%s 查询失败' % district)
            return False

    def retry(self, district, size, keyword, times, word):
        print(district + word, times)
        time.sleep(1)
        return self.LngLatBySearch(district, size, keyword, times)

    def ReverseAddress(self, location):
        '''
        通过腾讯地图API获取指定经纬度地址描述--逆地址解析接口
        :param location: 
        :return: 
        '''
        params = {
            'location': location,
            'get_poi': '1',
            'key': self.key
            }
        try:
            res = requests.get(self.api_reverse, params, timeout=10)
            time.sleep(1)
            return res.json()
        except Exception:
            print(traceback.format_exc())


if __name__ == '__main__':
    obj = GetLngLatTengxun()
    # geo = obj.LngLat('北京市北平食府（亦庄店）')
    geo = obj.LngLatBySearch('北京', 1, '北京市北平食府（亦庄店）', 0)
    # geo = obj.ReverseAddress('39.793949,116.588066')
    print(geo)
