#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_tym.py.py
@Author: Fengjicheng
@Date  : 2019/10/10
@Desc  : 根据通用名名称匹配三级类目字段
'''

import time
import json
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def add_cate(db_name, field, dyf_field):
    with open('dayaofang.json','r',encoding='utf-8') as f:
        daoyaofang = f.readlines()
    for i in tqdm(daoyaofang):
        dyf_content = json.loads(i)
        tym = dyf_content.get(dyf_field)
        leimu1Id = dyf_content.get('category1Id')
        leimu1Name = dyf_content.get('category1Name')
        leimu2Id = dyf_content.get('category2Id')
        leimu2Name = dyf_content.get('category2Name')
        leimu3Id = dyf_content.get('category3Id')
        leimu3Name = dyf_content.get('category3Name')
        food_list = find(db_name, {field: tym})
        for n in food_list:
            if not n.get('category1Id'):
                n['category1Id'] = leimu1Id
                n['category1Name'] = leimu1Name
                n['category2Id'] = leimu2Id
                n['category2Name'] = leimu2Name
                n['category3Id'] = leimu3Id
                n['category3Name'] = leimu3Name
                upsert_one(db_name, n)
        food_list.close()

if __name__ == '__main__':
    # add_cate('jyt_for_meddatebase', '通用名称', 'genericName')
    add_cate('jyt_for_meddatebase', '批准文号', 'authorizedNo')