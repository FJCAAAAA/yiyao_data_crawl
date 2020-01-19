#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CmekgForMed.py
@Author: Fengjicheng
@Date  : 2020/1/10
@Desc  : 药品库数据补充，输出药品数据
'''
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def cmekg_to_str(table):
    med_list = find(table, {})

    for med in med_list:
        med1 = med.copy()
        for k, v in med.items():
            if isinstance(v, list):
                med1[k] = '\n'.join(v)
        upsert_one(table, med1)
    med_list.close()
    print('{} 更新完成'.format(table))


def cmekg_for_med(table):
    med_list = find(table, {})
    num = 0
    for med in med_list:
        med1 = med.copy()
        for k, v in med.items():
            if k == '剂型':
                num += 1
                med1.pop(k)
                med1['药物剂型'] = v
        upsert_one(table, med1)
    med_list.close()
    print('{} 更新完成，共 {} 次'.format(table, num))

if __name__ == '__main__':
    # cmekg_to_str('cmekg_med')
    # cmekg_to_str('cmekg_dise')
    cmekg_for_med('cmekg_med')