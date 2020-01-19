#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_new.py.py
@Author: Fengjicheng
@Date  : 2019/10/26
@Desc  : 到家商品名称分析，补全通用名和规格
'''

import json
import re
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

pattern1 = re.compile(' ')
pattern2 = re.compile('（.*?）')
pattern3 = re.compile('\d+')

with open('jddj_new.json','r',encoding='utf-8') as f:
    Jddj = f.readlines()

for m in tqdm(Jddj):
    JddjDict = json.loads(m.strip())
    JddjName = JddjDict.get('名称')
    JddjTym = JddjDict.get('通用名')
    JddjGg = JddjDict.get('规格')
    JddjNameList = [x for x in re.split(' ',str(JddjName)) if x != '']
    JddjPingpai = JddjNameList[0]

    if len(JddjNameList) == 3 and pattern3.findall(JddjNameList[2]):
        if not JddjTym:
            JddjDict['通用名'] = JddjNameList[1]
        if not JddjGg:
            JddjDict['规格'] = JddjNameList[2]
        JddjDict['品牌名称'] = JddjNameList[0]

    insert('jddj_quan', JddjDict)
