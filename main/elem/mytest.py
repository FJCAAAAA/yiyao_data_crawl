#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : mytest.py
@Author: Fengjicheng
@Date  : 2019/12/25
@Desc  :
'''
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *
import time

sku_id_list_all = []
shop_list = find('elem_shop', {})
for shop in shop_list:
    sku_id_list_shop = []
    category_list = shop.get('category_list')
    if category_list:
        for category in category_list:
            sku_id_list = category.get('sku_id_list')
            sku_id_list_shop += sku_id_list
        sku_id_list_all += list(set(sku_id_list_shop))

sku_id_list_all_uniq = list(set(sku_id_list_all))

print(len(sku_id_list_all))
print(len(sku_id_list_all_uniq))

# sku总数：
# 5722791
# 5722791
