#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetFoodManual.py
@Author: Fengjicheng
@Date  : 2019/12/26
@Desc  : 第六步：获取商品说明书，并将 结果 更新到mongdo(elem_food_by_cate)
'''
import requests
import json
import urllib3
from config import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_food_manual(upc_ids):
    url = 'https://newretail.ele.me/newretail/drug/getupcdruginfos'
    data = {
        'upc_ids': upc_ids,
        # 'lng': lng,
        # 'lat': lat,
        # 'shardlocation': shardlocation
    }
    header = get_header()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = for_request(requests.get(url=url, params=data, headers=header, verify=False))
    if response:
        response_dict = json.loads(response.content.decode('utf-8'))
        result_dict = response_dict.get('result')
        if isinstance(result_dict, dict) and result_dict:
            manual = result_dict.get(upc_ids)
            return manual
        else:
            return {}


def get_all_food_manual():
    num = 0
    food_list = find('elem_food_by_cate', {})
    for food in food_list:
        num += 1
        if num > 121943:  # 从新的位置开始，如果第一次执行需要置为0
            try:
                manual = get_food_manual(food.get('upc_ids'))
            except Exception:
                print('upc_ids:{} 商品说明书爬取失败'.format(food.get('upc_ids')))
                print(traceback.format_exc())
                continue
            food['manual'] = manual
            upsert_one('elem_food_by_cate', food)
            print('###########{} 商品说明书爬取完成###########'.format(food.get('upc_name')))
    food_list.close()


if __name__ == '__main__':
    get_all_food_manual()
