#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Add_LngLat_Address_New.py
@Author: Fengjicheng
@Date  : 2019/11/6
@Desc  : 医院添加经纬度
'''

import json
import time
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.GetLngLatTengxun import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class AddLngLat(GetLngLatTengxun):

    def Hospital(self, filename, name_f, address_f, first_af, second_af, mongo_table):
        pattern1 = re.compile(';|,')
        pattern2 = '\((.*?)\)|(.*?):|的'
        zhixia_city = ['北京', '天津', '上海', '重庆']
        with open(filename, 'r', encoding='utf-8') as f:
            hopital_list = f.readlines()
        for n in tqdm(hopital_list):
            hopital_detail = json.loads(n)
            hopital_detail.pop('_id')
            name = hopital_detail.get(name_f)
            address = hopital_detail.get(address_f)
            first_area = hopital_detail.get(first_af)
            second_area = hopital_detail.get(second_af)
            address_list = re.split(pattern1,address)
            if len(address_list) == 1:
                address_detail = re.sub(pattern2, '', address_list[0])
                if first_area in zhixia_city:
                    if first_area in address_detail:
                        message1 = address_detail
                    else:
                        message1 = ''.join([first_area, address_detail])
                    if first_area in name:
                        message2 = name
                    else:
                        message2 = ''.join([first_area, name])
                else:
                    if second_area in address_detail:
                        message1 = address_detail
                    else:
                        message1 = ''.join([second_area, address_detail])
                    if second_area in name:
                        message2 = name
                    else:
                        message2 = ''.join([second_area, name])
                res_dict = self.LngLat(message2)
                if res_dict.get('status') == 0:
                    title = res_dict.get('result').get('title')
                    if title not in name and name not in title:
                    #说明通过名称搜索结果不正常，换地址搜索
                        res_dict = self.LngLat(message1)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name, address_list[0]))
                        continue
                else:
                    res_dict = self.LngLat(message1)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name, address_list[0]))
                        continue
                title = res_dict.get('result').get('title')
                location = res_dict.get('result').get('location')
                lat = location.get('lat')  # 纬度
                lng = location.get('lng')  # 经度
                hopital_detail['坐标码地址0'] = title
                hopital_detail['坐标码0'] = '%s,%s' % (lat, lng)
                insert(mongo_table, hopital_detail)
                time.sleep(1)
            else:
                for m in address_list:
                    address_detail = re.sub(pattern2, '', m)
                    if first_area in zhixia_city:
                        if first_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([first_area, address_detail])
                    else:
                        if second_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([second_area, address_detail])
                    res_dict = self.LngLat(message)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name, m))
                        continue
                    title = res_dict.get('result').get('title')
                    location = res_dict.get('result').get('location')
                    lat = location.get('lat')  # 纬度
                    lng = location.get('lng')  # 经度
                    hopital_detail['坐标码地址%d' % (address_list.index(m))] = title
                    hopital_detail['坐标码%d' % (address_list.index(m))] = '%s,%s' % (lat, lng)
                insert(mongo_table, hopital_detail)


obj = AddLngLat()
obj.Hospital('hospital_new.json','名称','地址','一级行政区','二级行政区','hospital_geo_address')