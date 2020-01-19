#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetFoodListByCategory.py
@Author: Fengjicheng
@Date  : 2019/12/26
@Desc  : ###new### 通过类别接口爬取商品详情 速度快###new###
        第五步：获取商品详情，并将 upc_ids(upc_id))、upc、upc_name、cat1_name、brand_name、Description、illustration、
        Photos、经纬度 更新到mongdo(elem_food_by_cate)
'''
import requests
import json
import urllib3
import traceback
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
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = for_request(requests.get(url=url, params=data, headers=header, verify=False))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        result_dict = response_dict.get('result')
        if isinstance(result_dict, dict):
            detail_list = result_dict.get('detail')
            food_list = result_dict.get('foods')

            if detail_list:
                for detail in detail_list:
                    food_list = detail.get('foods')
                    if food_list:
                        for food_detail in food_list:
                            try:
                                require_field = {'upc_ids': '', 'upc': '', 'upc_name': '', 'brand_name': '',
                                                 'description': '',
                                                 'illustration': '', 'photos': ''}
                                require_field['upc_ids'] = food_detail.get('upc_id')
                                require_field['upc'] = food_detail.get('upc')  # 条形码
                                require_field['upc_name'] = food_detail.get('upc_name')  # 商品名称
                                require_field['brand_name'] = food_detail.get('brand_name')  # 品牌
                                require_field['description'] = food_detail.get('description')
                                require_field['illustration'] = food_detail.get('illustration')
                                require_field['photos'] = [i.get('url') for i in food_detail.get('photos') if
                                                           isinstance(i, dict)]
                                insert('elem_food_by_cate', require_field)
                            except Exception:
                                print(traceback.format_exc())
                                continue

            if food_list:
                for food_detail in food_list:
                    try:
                        require_field = {'upc_ids': '', 'upc': '', 'upc_name': '', 'brand_name': '',
                                         'description': '',
                                         'illustration': '', 'photos': ''}
                        require_field['upc_ids'] = food_detail.get('upc_id')
                        require_field['upc'] = food_detail.get('upc')  # 条形码
                        require_field['upc_name'] = food_detail.get('upc_name')  # 商品名称
                        require_field['brand_name'] = food_detail.get('brand_name')  # 品牌
                        require_field['description'] = food_detail.get('description')
                        require_field['illustration'] = food_detail.get('illustration')
                        require_field['photos'] = [i.get('url') for i in food_detail.get('photos') if
                                                   isinstance(i, dict)]
                        insert('elem_food_by_cate', require_field)
                    except Exception:
                        print(traceback.format_exc())
                        continue



def get_all_food_list():
    shop_list = find('elem_shop', {})
    num = 0
    for shop in shop_list:
        num += 1
        if num > 5677:  # 从新的门店开始，如果第一次执行需要置为0
            print('###########{} 门店商品详情开始爬取 BY CATE###########'.format(shop.get('shop_name')))
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
                    try:
                        if len(category_id_list) > 3:
                            # 为保证获取全量的商品列表，category_id每次传入个数最大为三个
                            step = 3
                            for i in range(0, len(category_id_list), step):
                                get_food_list(','.join(category_id_list[i:i + step]), shop_id, type_, lng, lat, shardlocation)

                        else:
                            get_food_list(category_id, shop_id, type_, lng, lat, shardlocation)
                    except Exception:
                        print(traceback.format_exc())
                        continue

    shop_list.close()


if __name__ == '__main__':
    get_all_food_list()
