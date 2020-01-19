#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AddBrand.py
@Author: Fengjicheng
@Date  : 2020/1/13
@Desc  :
'''
import json
import re
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

pattern1 = re.compile(' ')
pattern2 = re.compile('（.*?）|（.*')
pattern3 = re.compile('\d+')


# with open('jddj_quan.json','r',encoding='utf-8') as f:
#     Jddj = f.readlines()

with open('D:\project\yiyao_data_crawl\yiyao_data_crawl\main\jddj_add\quan\jddj_pingpai_uniq.json','r',encoding='utf-8') as f:
    Pingpai = f.readlines()

jyt = find('jyt_for_pljp', {})

for m in jyt:
    for n in tqdm(Pingpai):
        PingpaiDict = json.loads(n.strip())
        PingpaiName = str(PingpaiDict.get('品牌名称'))
        PingpaiNameX = re.sub(pattern2, '', str(PingpaiName))
        PingpaiId = PingpaiDict.get('品牌id')
        JddjName = m.get('生产厂家')
        if PingpaiNameX in JddjName:
            m['品牌名称'] = PingpaiName
            m['品牌ID'] = PingpaiId
            upsert_one('jyt_for_pljp', m)

jyt.close()
