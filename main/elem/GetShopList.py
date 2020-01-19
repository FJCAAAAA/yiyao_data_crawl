#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetShopList.py
@Author: Fengjicheng
@Date  : 2019/12/25
@Desc  : 第二步：获取指定地点医药数据门店，并将 门店名称、shop_id、经纬度 写入mongodb(elem_shop)
'''
import requests
import json
import time
from tqdm import tqdm
from config import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_shop_list(lng, lat, city):
    url = 'https://newretail.ele.me/newretail/main/shoplist'
    shardlocation = ','.join([lng,lat])
    data = {
        'cat_id': '0',
        'channel': 'health',
        'fromalipay': '0',
        'pn': '1',
        'rn': '10',
        'rule_id': '0',
        'scene_id': '0',
        'scene_type': 'shop',
        'sortby': '',
        'type': '1',
        'user_type': 'auto',
        'window': '3',
        'lng': lng,
        'lat': lat,
        'shardlocation': shardlocation
    }
    header = get_header()
    response = for_request(requests.get(url=url, params=data, headers=header))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        shop_list = response_dict.get('result').get('shop_list')
        if shop_list:
            for shop in shop_list:
                require_field = {'city': city, 'shop_name': '', 'shop_id': '', 'logo_url': '', 'lng': lng, 'lat': lat,
                                 'shardlocation': shardlocation}
                shop_info = shop.get('shop_info')
                require_field['shop_name'] = shop_info.get('shop_name')
                require_field['shop_id'] = shop_info.get('wid')
                require_field['logo_url'] = shop_info.get('logo_url')
                insert('elem_shop', require_field)
        else:
            print('lng: {},lat: {} 不存在门店'.format(lng, lat))

    else:
        print('lng: {},lat: {} 请求失败'.format(lng, lat))


def get_all_shop_list():
    with open('txt/districts.txt', 'r', encoding='utf-8') as f:
        geocode_list = f.readlines()
    for geocode in tqdm(geocode_list):
        geocode_dict = json.loads(geocode.strip())
        for city, geocode_dict_all in geocode_dict.items():
            print('开始爬取 {} 地区门店'.format(city))
            if geocode_dict_all:
                for k, v in geocode_dict_all.items():
                    lng = str(v.get('lng'))
                    lat = str(v.get('lat'))
                    get_shop_list(lng=lng, lat=lat, city=city)
                    time.sleep(1)


if __name__ == '__main__':
    get_all_shop_list()
