#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : SupppGeoOfHospital.py
@Author: Fengjicheng
@Date  : 2019/12/31
@Desc  : 针对坐标码0 为空的，按照医院名称搜索
'''

import json
import time
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.GetLngLatTengxun import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

def supply_geo():
    hospital = find('hospital_zhushuju_geo',{"坐标码0":""})
    for data in hospital:
        zhixia_city = ['北京', '天津', '上海', '重庆']
        name = data.get('医院名称')
        first_area = data.get('所在省')
        second_area = data.get('所在市')
        if first_area in zhixia_city:
            message = ''.join([first_area, name])
        else:
            message = ''.join([second_area, name])
        obj = GetLngLatTengxun()
        res_dict = obj.LngLat(message)
        if res_dict.get('status') != 0:
            print('%s 经纬度获取失败' % (name))
            continue
        title = res_dict.get('result').get('title')
        location = res_dict.get('result').get('location')
        lat = location.get('lat')  # 纬度
        lng = location.get('lng')  # 经度
        data['坐标码0'] = '%s,%s' % (lat, lng)
        upsert_one('hospital_zhushuju_geo', data)
        print('{} 更新完成'.format(name))
    hospital.close()


if __name__ == '__main__':
    supply_geo()