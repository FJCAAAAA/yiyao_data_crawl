#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetDistrictsByTengxun.py
@Author: Fengjicheng
@Date  : 2019/12/25
@Desc  : 第一步：通过腾讯地图获得所有一线、二线、三线、四线及五线城市的小区（每个城市20个）
'''
from yiyao_data_crawl.main.common.GetDistrictsTengxun import SearchDistricts


def get_districts():
    obj = SearchDistricts()
    city_num = 0
    city_level = 0
    with open('txt/cities.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            city_level += 1
            cities_list = i.strip().split('、')
            city_num += len(cities_list)
            print('开始查询 %d' % city_level)
            obj.get_all(cities_list, 'txt/districts.txt')
    print('查询完毕，总共 %d 个城市。' % city_num)
    obj.get_all(['吉林市'], 'txt/districts.txt')


if __name__ == '__main__':
    get_districts()
