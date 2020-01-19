#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Add_LngLat.py
@Author: Fengjicheng
@Date  : 2019/10/28
@Desc  : 医院添加经纬度，通过名称查询
'''

import json
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.Get_LngLat_Tengxun import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

# obj = GetLngLatTengxun()
# obj.LngLat('北京中日友好医院','FRJBZ-UIUWW-LPFRQ-OAX22-GJFD3-WPBRA')

class AddLngLat(GetLngLatTengxun):
    def Hospital(self):
        zhixia_city = ['北京','天津','上海','重庆']
        with open('hospital.json','r',encoding='utf-8') as f:
            hopital_list = f.readlines()
        for n in tqdm(hopital_list):
            hopital_detail = json.loads(n)
            hopital_detail.pop('_id')
            name = hopital_detail.get('名称')
            address = hopital_detail.get('地址 ')
            first_area = hopital_detail.get('一级行政区')
            second_area = hopital_detail.get('二级行政区')
            if first_area in zhixia_city:   #腾讯地图地址转换API必须要携带城市，为了保证查询结果准确，直辖市的包括一级和二级，非直辖市的只有二级
                message1 = ''.join([first_area,second_area,name])
            else:
                message1 = ''.join([second_area,name])
            message2 = address
            res_dict = self.LngLat(message1)
            if res_dict.get('status') != 0:
                res_dict = self.LngLat(message2)
                if res_dict.get('status') != 0:
                    print('%s 经纬度获取失败' %(name))
                    continue
            title = res_dict.get('result').get('title')
            location = res_dict.get('result').get('location')
            lat = location.get('lat') #纬度
            lng = location.get('lng') #经度
            hopital_detail['坐标码地址'] = title
            hopital_detail['坐标码'] = '%s,%s' %(lat,lng)
            insert('hospital_geo',hopital_detail)
            time.sleep(1)
            # print(hopital_detail)
            # time.sleep(5)

    def HospitalAvailable(self):
        zhixia_city = ['北京','天津','上海','重庆']
        with open('hospital_available.json','r',encoding='utf-8') as f:
            hopital_list = f.readlines()
        for n in tqdm(hopital_list):
            hopital_detail = json.loads(n)
            hopital_detail.pop('_id')
            name = hopital_detail.get('医院名称')
            name1 = hopital_detail.get('医院别名')
            address = hopital_detail.get('医院地址')
            first_area = hopital_detail.get('所在省')
            second_area = hopital_detail.get('所在市')
            # 腾讯地图地址转换API必须要携带城市，为了保证查询结果准确，直辖市的包括一级和二级，非直辖市的只有二级
            if first_area in zhixia_city:
                message1 = ''.join([first_area,second_area,name])
            else:
                message1 = ''.join([second_area,name])
            message2 = address
            res_dict = self.LngLat(message1)
            if res_dict.get('status') != 0:
                res_dict = self.LngLat(message2)
                if res_dict.get('status') != 0:
                    print('%s 经纬度获取失败' %(name))
                    continue
            title = res_dict.get('result').get('title')
            if name != title:
                if first_area in zhixia_city:
                    message1 = ''.join([first_area, second_area, name1])
                else:
                    message1 = ''.join([second_area, name1])
                message2 = address
                res_dict = self.LngLat(message1)
                if res_dict.get('status') != 0:
                    res_dict = self.LngLat(message2)
                    if res_dict.get('status') != 0:
                        print('%s 经纬度获取失败' % (name))
                        continue
                title = res_dict.get('result').get('title')

            location = res_dict.get('result').get('location')
            # 纬度
            lat = location.get('lat')
            # 经度
            lng = location.get('lng')
            hopital_detail['坐标码地址'] = title
            hopital_detail['坐标码'] = '%s,%s' %(lat,lng)
            insert('hospital_available_geo',hopital_detail)
            time.sleep(1)
            # print(hopital_detail)
            # time.sleep(5)





obj = AddLngLat()
# obj.Hospital()
obj.HospitalAvailable()

