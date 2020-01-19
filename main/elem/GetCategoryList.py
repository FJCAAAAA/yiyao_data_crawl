#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetCategoryList.py
@Author: Fengjicheng
@Date  : 2019/12/25
@Desc  : 第三步：获取门店类别列表，并将 类别名称、category_id、type 更新到mongdo(elem_shop)
'''
import requests
import json
import time
from tqdm import tqdm
from config import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_cate_list(shop_id, lng, lat, shardlocation):
    url = 'https://newretail.ele.me/newretail/shop/getshopcategoryinfo'
    data = {
        'shop_id': shop_id,
        'sku_id': '',
        'lng': lng,
        'lat': lat,
        'shardlocation': shardlocation
    }
    header = get_header()
    response = for_request(requests.get(url=url, params=data, headers=header))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        category_list = response_dict.get('result')
        if category_list:
            require_field_list = []
            for cate in category_list:
                # require_field = {'category_id': cate.get('id'), 'shop_id': shop_id, 'type': cate.get('type'),
                #                  'lng': lng, 'lat': lat, 'shardlocation': shardlocation}
                require_field = {'category_name': cate.get('name'), 'category_id': cate.get('id'),
                                 'type': cate.get('type')}
                require_field_list.append(require_field)
            return require_field_list


def get_all_cate_list():
    shop_list = find('elem_shop', {})
    for shop in shop_list:
        cate_list = get_cate_list(shop.get('shop_id'), shop.get('lng'), shop.get('lat'), shop.get('shardlocation'))
        shop['category_list'] = cate_list
        upsert_one('elem_shop', shop)
        print('###########{} 门店类别列表更新完成###########'.format(shop.get('shop_name')))
        time.sleep(1)

if __name__ == '__main__':
    # print(get_cate_list('1929623455', '116.56297199428082', '39.78667499497533', '116.56297199428082,39.78667499497533'))
    get_all_cate_list()
