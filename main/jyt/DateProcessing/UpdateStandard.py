#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : UpdateStandard.py
@Author: Fengjicheng
@Date  : 2020/1/9
@Desc  : 规格更新
'''
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def update_standard():
    ypk_food_list = find('jyt_for_meddatebase', {'规格': '复方'})
    for ypk_food in ypk_food_list:
        drugId = ypk_food.get('drugId')
        jyt_food_list = find('jyt', {'drugId': drugId})
        for jyt_food in jyt_food_list:
            standard = jyt_food.get('drugDesc').get('standard')
            if standard:
                ypk_food['规格'] = standard
                upsert_one('jyt_for_meddatebase', ypk_food)
        jyt_food_list.close()
    ypk_food_list.close()

if __name__ == '__main__':
    update_standard()
