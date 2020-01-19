#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GeoAccuracyVerify.py
@Author: Fengjicheng
@Date  : 2020/1/2
@Desc  : 通过腾讯地图逆地址解析，验证经纬度准确率
'''

from yiyao_data_crawl.main.common.GetLngLatTengxun import GetLngLatTengxun
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def all_geo_verify():
    hos_list = find('hospital_zhushuju_geo', {})
    file = open('hospital_geo_verify.txt', 'a', encoding='utf-8')
    for hos in hos_list:
        name = hos.get('医院名称')
        lnglat = hos.get('坐标码0')
        obj = GetLngLatTengxun()
        lnglat_dict = obj.ReverseAddress(lnglat)
        # 判断请求是否成功
        if lnglat_dict.get('status') != 0:
            print('{} 医院经纬度逆地址解析失败'.format(name))
            continue
        opi_list = lnglat_dict.get('result').get('pois')
        opi_title_list = []
        for opi in opi_list:
            opi_title_list.append(opi.get('title'))
        if name not in opi_title_list:
            file.write(name + '\n')
            file.flush()
        print('{} 医院经纬度检查完成'.format(name))
    file.close()
    hos_list.close()

if __name__ == '__main__':
    all_geo_verify()
