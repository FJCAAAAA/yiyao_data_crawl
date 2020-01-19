#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetFoodListByCategory.py
@Author: Fengjicheng
@Date  : 2019/12/26
@Desc  : 第四步：获取商品列表，并将 sku_id 更新到mongdo(elem_shop)
'''
import requests
import json
import time
from tqdm import tqdm
from config import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_food_list(category_id, shop_id, type, lng, lat, shardlocation):
    url = 'https://newretail.ele.me/newretail/shop/getfoodsbycategory'
    data = {
        'category_id': category_id,
        'shop_id': shop_id,
        'type': type,
        'lng': lng,
        'lat': lat,
        'shardlocation': shardlocation
    }
    header = get_header()
    response = for_request(requests.get(url=url, params=data, headers=header))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        result_dict = response_dict.get('result')
        if isinstance(result_dict, dict):
            detail_list = result_dict.get('detail')
            food_list = result_dict.get('foods')
            sku_id_list = []
            if detail_list:
                for detail in detail_list:
                    food_list = detail.get('foods')
                    if food_list:
                        for food in food_list:
                            sku_id = food.get('sku_id')
                            if sku_id:
                                sku_id_list.append(sku_id)
            if food_list:
                for food in food_list:
                    sku_id = food.get('sku_id')
                    if sku_id:
                        sku_id_list.append(sku_id)
            return sku_id_list



def get_all_food_list():
    shop_list = find('elem_shop', {})
    num = 0
    for shop in shop_list:
        num += 1
        if num > 0:  # 从新的位置开始，如果第一次执行需要置为0
            shop_id = shop.get('shop_id')
            lng = shop.get('lng')
            lat = shop.get('lat')
            shardlocation = shop.get('shardlocation')
            category_list = shop.get('category_list')
            if category_list:
                for index, category in enumerate(category_list):
                    type_ = category.get('type')
                    category_id = category.get('category_id')
                    category_id_list = category_id.split(',')
                    sku_id_list = []
                    if len(category_id_list) > 3:
                        # 为保证获取全量的商品列表，category_id每次传入个数最大为三个
                        step = 3
                        for i in range(0, len(category_id_list), step):
                            sku_id_list_1 = get_food_list(','.join(category_id_list[i:i + step]), shop_id, type_, lng, lat, shardlocation)
                            if sku_id_list_1:
                                sku_id_list += sku_id_list_1
                            # time.sleep(1)
                    else:
                        sku_id_list = get_food_list(category_id, shop_id, type_, lng, lat, shardlocation)
                        # time.sleep(1)
                    if sku_id_list:
                        sku_id_list = list(set(sku_id_list))
                        shop['category_list'][index]['sku_id_list'] = sku_id_list
                    else:
                        shop['category_list'][index]['sku_id_list'] = []
                        print('{} 类别商品列表为空'.format(category.get('category_name')))
                upsert_one('elem_shop', shop)
                print('###########{} 商品列表更新完成###########'.format(shop.get('shop_name')))


if __name__ == '__main__':
    get_all_food_list()
