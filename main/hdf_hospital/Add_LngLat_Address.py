#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Add_LngLat_Address.py
@Author: Fengjicheng
@Date  : 2019/11/4
@Desc  : 医院添加经纬度，先判断地址是否唯一，1.如果地址唯一，使用一个地址搜索 2.如果地址不唯一，按照地址列表搜索
'''

import json
import time
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.GetLngLatTengxun import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class AddLngLat(GetLngLatTengxun):

    def Hospital(self):
        pattern1 = re.compile(';|,')
        pattern2 = '\((.*?)\)|(.*?):|的'
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
            address_list = re.split(pattern1,address)
            if len(address_list) == 1:
                #说明地址唯一
                address_detail = re.sub(pattern2, '', address_list[0])
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
                    print('%s 经纬度获取失败' %(name))
                    continue
                title = res_dict.get('result').get('title')
                location = res_dict.get('result').get('location')
                lat = location.get('lat') #纬度
                lng = location.get('lng') #经度
                hopital_detail['坐标码地址0'] = title
                hopital_detail['坐标码0'] = '%s,%s' %(lat,lng)
                insert('hospital_geo_address',hopital_detail)
                time.sleep(1)
            else:
                #说明地址不唯一
                for m in address_list:
                    address_detail = re.sub(pattern2, '', m)
                    if first_area in zhixia_city:
                        if first_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([first_area,address_detail])
                    else:
                        if second_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([second_area,address_detail])
                    res_dict = self.LngLat(message)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name,m))
                        continue
                    title = res_dict.get('result').get('title')
                    location = res_dict.get('result').get('location')
                    lat = location.get('lat')  # 纬度
                    lng = location.get('lng')  # 经度
                    hopital_detail['坐标码地址%d'%(address_list.index(m))] = title
                    hopital_detail['坐标码%d'%(address_list.index(m))] = '%s,%s' % (lat, lng)
                insert('hospital_geo_address', hopital_detail)
                time.sleep(1)

    def HospitalAvailable(self):
        pattern1 = re.compile(';|,')
        pattern2 = '\((.*?)\)|(.*?):|的'
        # pattern3 = re.compile('(.*?):')
        # pattern4 =  re.compile('的')
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
            address_list = re.split(pattern1, address)
            if len(address_list) == 1:
                address_detail = re.sub(pattern2, '', address_list[0])
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
                # if res_dict.get('status') != 0:
                #     res_dict = self.LngLat(message2)
                if res_dict.get('status') != 0:
                    print('%s 经纬度获取失败' %(name))
                    continue
                title = res_dict.get('result').get('title')
                location = res_dict.get('result').get('location')
                # 纬度
                lat = location.get('lat')
                # 经度
                lng = location.get('lng')
                hopital_detail['坐标码地址0'] = title
                hopital_detail['坐标码0'] = '%s,%s' %(lat,lng)
                insert('hospital_available_geo_address',hopital_detail)
                time.sleep(1)
                # print(hopital_detail)
                # time.sleep(5)
            else:
                for m in address_list:
                    address_detail = re.sub(pattern2, '', m)
                    if first_area in zhixia_city:
                        if first_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([first_area,address_detail])
                    else:
                        if second_area in address_detail:
                            message = address_detail
                        else:
                            message = ''.join([second_area,address_detail])
                    res_dict = self.LngLat(message)
                    if res_dict.get('status') != 0:
                        print('%s %s 经纬度获取失败' % (name,m))
                        continue
                    title = res_dict.get('result').get('title')
                    location = res_dict.get('result').get('location')
                    lat = location.get('lat')  # 纬度
                    lng = location.get('lng')  # 经度
                    hopital_detail['坐标码地址%d'%(address_list.index(m))] = title
                    hopital_detail['坐标码%d'%(address_list.index(m))] = '%s,%s' % (lat, lng)
                insert('hospital_available_geo_address', hopital_detail)
                time.sleep(1)

obj = AddLngLat()
obj.Hospital()
# obj.HospitalAvailable()