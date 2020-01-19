#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetFoodDetail.py
@Author: Fengjicheng
@Date  : 2019/12/26
@Desc  : 第五步：获取商品详情，并将 upc_ids(upc_id))、upc、upc_name、cat1_name、brand_name、Description、illustration、
        Photos、经纬度 更新到mongdo(elem_food)
'''
import requests
import json
import traceback
from tqdm import tqdm
from config import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_food_detail(shop_id, sku_id, lng, lat, shardlocation):
    url = 'https://newretail.ele.me/newretail/shop/getgoodsdetail'
    data = {
        'plat': 'bdwm',
        'shop_id': shop_id,
        'sku_id': sku_id,
        'lng': lng,
        'lat': lat,
        'shardlocation': shardlocation
    }
    header = get_header()
    response = for_request(requests.get(url=url, params=data, headers=header))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        result_list = response_dict.get('result')
        require_field = {'upc_ids': '', 'upc': '', 'upc_name': '', 'brand_name': '', 'description': '',
                         'illustration': '', 'photos': ''}
        if isinstance(result_list, list) and result_list:
            food_detail = result_list[0]
            require_field['upc_ids'] = food_detail.get('upc_id')
            require_field['upc'] = food_detail.get('upc')  # 条形码
            require_field['upc_name'] = food_detail.get('upc_name')  # 商品名称
            require_field['brand_name'] = food_detail.get('brand_name')  # 品牌
            require_field['description'] = food_detail.get('description')
            require_field['illustration'] = food_detail.get('illustration')
            require_field['photos'] = [i.get('url') for i in food_detail.get('photos') if isinstance(i, dict)]
        return require_field


def get_all_food_detail():
    num = 0
    shop_list = find('elem_shop', {})
    for shop in shop_list:
        num += 1
        if num > 62:  # 从新的门店开始，如果第一次执行需要置为0
            print('###########{} 门店商品详情开始爬取###########'.format(shop.get('shop_name')))
            shop_id = shop.get('shop_id')
            lng = shop.get('lng')
            lat = shop.get('lat')
            shardlocation = shop.get('shardlocation')
            category_list = shop.get('category_list')
            if category_list:
                sku_id_list = []
                for index, category in enumerate(category_list):
                    sku_id_list += category.get('sku_id_list')
                sku_id_list = list(set(sku_id_list))
                if sku_id_list:
                    for sku_id in sku_id_list:
                        try:
                            require_field = get_food_detail(shop_id, sku_id, lng, lat, shardlocation)
                            require_field['lng'] = lng
                            require_field['lat'] = lat
                            require_field['shardlocation'] = shardlocation
                            insert('elem_food', require_field)
                        except Exception:
                            print('shop_id:{},sku_id:{} 商品详情爬取失败'.format(shop_id, sku_id))
                            print(traceback.format_exc())
                            continue

if __name__ == '__main__':
    get_all_food_detail()
