#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_pp.py
@Author: Fengjicheng
@Date  : 2019/10/25
@Desc  :到家数据添加品牌字段，方法：判断到家数据名称中是否包含品牌名称
'''

import json
import re
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

pattern1 = re.compile(' ')
pattern2 = re.compile('（.*?）|（.*')
pattern3 = re.compile('\d+')


with open('jddj_quan.json','r',encoding='utf-8') as f:
    Jddj = f.readlines()

with open('jddj_pingpai_uniq.json','r',encoding='utf-8') as f:
    Pingpai = f.readlines()

# for i in Pingpai:
#     print(type(json.loads(i.strip())))
#     time.sleep(3)

for n in tqdm(Pingpai):
    PingpaiDict = json.loads(n.strip())
    PingpaiName = str(PingpaiDict.get('品牌名称'))
    PingpaiNameX = re.sub(pattern2,'',str(PingpaiName))
    PingpaiId = PingpaiDict.get('品牌id')

    for m in Jddj:
        JddjDict = json.loads(m.strip())
        JddjName = JddjDict.get('名称')
        JddjNameList = [x for x in re.split(' ', str(JddjName)) if x != '']
        if PingpaiName in JddjNameList or PingpaiNameX in JddjNameList:
            JddjDict['品牌名称'] = PingpaiName
            JddjDict['品牌ID'] = PingpaiId
            upsert_one('jddj_quan',JddjDict)
        else:
            continue



        # JddjTym = JddjDict.get('通用名')
        # JddjGg = JddjDict.get('规格')
        #
        # JddjNameList = [x for x in re.split(' ',str(JddjName)) if x != '']
        # JddjPingpai = JddjNameList[0]
        # if JddjPingpai == PingpaiNameX:
        #     JddjDict['品牌名称'] =  PingpaiName
        #     JddjDict['品牌ID'] = PingpaiId
        #     if len(JddjNameList) == 3 and pattern3.findall(JddjNameList[2]):
        #         if not JddjTym:
        #             JddjDict['通用名'] = JddjNameList[1]
        #         if not JddjGg:
        #             JddjDict['规格'] = JddjNameList[2]
        #     insert('jddj_add_pingpai',JddjDict)
        # else:
        #     continue
