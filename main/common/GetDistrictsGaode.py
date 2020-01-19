#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_districts_ll.py.py
@Author: Fengjicheng
@Date  : 2019/9/9
@Desc  : 通过高德地图API获取指定城市行政区域及坐标
'''
import requests
import time
import json


def geocode_districts(distict, times):
    if times > 9:
        return 0
    times = times + 1
    url = 'https://restapi.amap.com/v3/config/district'
    parameters = {
        'key': '',
        'keywords': distict,
        'subdistrict': 3,
        'extensions': 'base'
    }
    try:
        response = requests.get(url, params=parameters, timeout=10)
    except Exception as e:
        return retry(distict, times, '%s,try again' % (e))
    content = response.json()
    if content['status'] == '1':
        disticts_dict = {}
        distict1 = content['districts'][0]
        if distict1['level'] == 'province':
            distict2 = distict1['districts'][0]
            for n in distict2['districts']:
                for m in n['districts']:
                    disticts_dict[m['name']] = m['center']
        elif distict1['level'] == 'city':
            for n in distict1['districts']:
                if n['districts']:
                    for m in n['districts']:
                        disticts_dict[m['name']] = m['center']
                else:
                    disticts_dict[n['name']] = n['center']
        elif distict1['level'] == 'district':
            for n in distict1['districts']:
                disticts_dict[n['name']] = n['center']
        print('%s 行政区域获取成功' % (distict))
        return json.dumps(disticts_dict, ensure_ascii=False)
    else:
        print('返回失败')


def retry(distict,times,word):
    print(distict + word, times)
    time.sleep(1)
    return geocode_districts(distict,times)
