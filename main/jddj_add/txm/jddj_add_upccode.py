#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_upccode.py
@Author: Fengjicheng
@Date  : 2019/10/17
@Desc  :
'''
import re
import json
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

with open('upcCode.txt','r',encoding='utf-8') as f:
    upcCode = f.readline()
with open('jddj_skuId_new.json','r',encoding='utf-8') as f:
    jddj_sku = f.readlines()
# print(len(jddj_sku))
# file = open('jddj_upcCode.json','a',encoding='utf-8')

pattern1 = '{.*?}'
spe1 = re.compile(pattern1)

upcCode_list = spe1.findall(upcCode)

for n in tqdm(upcCode_list):
    upcCode_dict = json.loads(n)
    if 'upcCode' in upcCode_dict:
        # print(n)
        for m in jddj_sku:
            jddj_sku_dict = json.loads(m)
            if jddj_sku_dict.get('skuId') == upcCode_dict['skuId']:
                jddj_sku_dict['upcCode'] = upcCode_dict['upcCode']
                insert('jddj_upcCode',jddj_sku_dict)
                # file.write(json.dumps(jddj_sku_dict,ensure_ascii=False) + '\n')
                # file.flush()
# file.close()

