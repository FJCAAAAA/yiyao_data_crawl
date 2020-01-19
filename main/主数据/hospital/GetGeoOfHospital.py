#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetGeoOfHospital.py
@Author: Fengjicheng
@Date  : 2019/12/30
@Desc  : 通过腾讯接口获取主数据经纬度
'''
import json
import time
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.GetLngLatTengxun import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class AddLngLat(GetLngLatTengxun):

    def Hospital(self, filename, name_f, address_f, first_af, second_af, mongo_table):
        pattern1 = re.compile(';|,|；')
        pattern2 = '\((.*?)\)|(.*?):|的'
        pattern3 = re.compile('市|县')
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
            if isinstance(address, str):
                address_list = re.split(pattern1, address)
            else:
                address_list = [address]
            if len(address_list) == 1:
                # address_detail = re.sub(pattern2, '', address_list[0])
                # 判断是否是直辖市
                if first_area in zhixia_city:
                    region = first_area
                else:
                    region = second_area
                if region:
                    geo = self.LngLatBySearch(region, 1, name, 0)
                else:
                    name_split = pattern3.split(name)
                    if len(name_split) > 1:
                        region = name_split[0]
                        geo = self.LngLatBySearch(region, 1, name, 0)
                    else:
                        res_dict = self.LngLat(address)
                        if res_dict.get('status') != 0:
                            print('%s %s 经纬度获取失败' % (name, address))
                            continue
                        title = res_dict.get('result').get('title')
                        location = res_dict.get('result').get('location')
                        lat = location.get('lat')  # 纬度
                        lng = location.get('lng')  # 经度
                        geo = '%s,%s' % (lat, lng)
                hopital_detail['坐标码0'] = geo
            else:
                for m in address_list:
                    addr = ''.join([first_area, second_area, re.sub(pattern2, '', m)])
                    res_dict = self.LngLat(addr)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name, m))
                        continue
                    title = res_dict.get('result').get('title')
                    location = res_dict.get('result').get('location')
                    lat = location.get('lat')  # 纬度
                    lng = location.get('lng')  # 经度
                    # hopital_detail['坐标码地址%d' % (address_list.index(m))] = title
                    hopital_detail['坐标码%d' % (address_list.index(m))] = '%s,%s' % (lat, lng)
            insert(mongo_table, hopital_detail)


if __name__ == '__main__':
    obj = AddLngLat()
    obj.Hospital('hospital_zhushuju.json', '医院名称', '医院地址','所在省','所在市', 'hospital_zhushuju_geo')