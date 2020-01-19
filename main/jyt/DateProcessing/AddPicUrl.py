#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AddPicUrl.py
@Author: Fengjicheng
@Date  : 2020/1/9
@Desc  : 图片链接查询，添加到药品库数据
'''

from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def ypk_add_picurl():
    num = 0
    jyt_food_list = find('jyt', {})
    for jyt_food in jyt_food_list:
        num += 1
        drugId = jyt_food.get('drugId')
        print('第 {} 个，drugId：{}'.format(num, drugId))
        ypPics = jyt_food.get('ypPics')
        url_head = 'http://ydapi.yjj.beijing.gov.cn/static/'
        ypPics = [url_head+x for x in ypPics]

        ypk_food_list = find('jyt_for_meddatebase', {'drugId': drugId})
        for ypk_food in ypk_food_list:
            ypk_food['图片'] = ypPics
            upsert_one('jyt_for_meddatebase', ypk_food)
        ypk_food_list.close()
    jyt_food_list.close()

if __name__ == '__main__':
    ypk_add_picurl()

