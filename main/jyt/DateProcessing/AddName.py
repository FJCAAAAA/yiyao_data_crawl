#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AddName.py
@Author: Fengjicheng
@Date  : 2020/1/13
@Desc  :
'''
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *
import time

jyt = find('jyt_for_pljp', {})
for med in jyt:
    med_brand = med.get('品牌名称')
    med_gname = med.get('通用名称')
    med_pack = med.get('包装')
    if med_brand:
        med['名称'] = ' '.join([med_gname, med_pack])
        print(med.get('名称'))
        # time.sleep(1)
        upsert_one('jyt_for_pljp', med)

jyt.close()