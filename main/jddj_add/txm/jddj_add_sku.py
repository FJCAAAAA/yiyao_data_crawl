#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_txm.py
@Author: Fengjicheng
@Date  : 2019/10/11
@Desc  :
'''

import time
import json
import re
import traceback
from tqdm import tqdm
from functools import reduce
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

#乘法
def chengfa(mylist):
    if mylist:
        return reduce(lambda x, y: x * y, mylist)

#规格对比
def compare(mylist1,mylist2):
    if mylist1 == mylist2:
        return 1
    elif chengfa(mylist1)  == chengfa(mylist2):
        return 1
    elif not [False for num in mylist1 if num not in mylist2]:
        return 1
    elif not [False for num in mylist2 if num not in mylist1]:
        return 1


pattern = '\d+'
with open('jddj_leimu_new.json','r',encoding='utf-8') as f:
    jddj_leimu = f.readlines()
for n in tqdm(jddj_leimu):
    jddj_content = json.loads(n)
    jddj_pzwh = jddj_content['批准文号']
    jddj_gg = jddj_content['规格']
    jddj_name = jddj_content['名称']
    try:
        jddj_gg_num = re.findall(pattern,jddj_gg)
        jddj_name_num = re.findall(pattern,jddj_name)
    except Exception:
        print("jddj规格匹配失败",jddj_content)
        continue
    jddj_gg_num_list = [int(x) for x in jddj_gg_num]
    jddj_name_num_list = [int(x) for x in jddj_name_num]
    for m in find('dayaofang',{'authorizedNo':jddj_pzwh}):
        dayaofang_sku = m['skuId']
        dayaofang_gg = m['specification']
        dayaofang_name = m['skuName']
        try:
            dayaofang_gg_num = re.findall(pattern,dayaofang_gg)
            dayaofang_name_num = re.findall(pattern,dayaofang_name)
        except Exception:
            print("dayaofang规格匹配失败",dayaofang_sku)
            break
        dayaofang_gg_num_list = [int(x) for x in dayaofang_gg_num]
        dayaofang_name_num_list = [int(x) for x in dayaofang_name_num]
        if compare(jddj_gg_num_list,dayaofang_gg_num_list) or compare(jddj_name_num_list,dayaofang_name_num_list):
            jddj_content['skuId'] = str(dayaofang_sku)
            try:
                upsert_one('jddj_leimu_new', jddj_content)
            except Exception:
                print(traceback.format_exc())
            break
        else:
            continue







