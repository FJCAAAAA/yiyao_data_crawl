#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_txm.py
@Author: Fengjicheng
@Date  : 2019/11/20
@Desc  : ziying与315数据匹配，添加条形码
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


pattern = '[\d+\.\d]*'
with open('ziying.json','r',encoding='utf-8') as f:
    ziying = f.readlines()
for n in tqdm(ziying):
    jddj_content = json.loads(n)
    jddj_content.pop("_id")
    jddj_content['upcCode'] = ''
    jddj_pzwh = jddj_content.get('批准文号')
    jddj_gg = jddj_content.get('规格')
    jddj_name = jddj_content.get('药品Sku名称')
    jddj_tym = jddj_content.get('药品名称')
    jddj_pp = jddj_content.get('生产厂家')
    try:
        jddj_gg_num = re.findall(pattern,jddj_gg)
        # jddj_name_num = re.findall(pattern,jddj_name)
    except Exception:
        print("jddj规格匹配失败",jddj_content)
        continue
    jddj_gg_num_list = [float(re.sub('\+','',x)) for x in jddj_gg_num if re.sub('\+','',x) and x != '.']
    # jddj_name_num_list = [float(re.sub('\+','',x)) for x in jddj_name_num if re.sub('\+','',x) and x != '.']
    if jddj_pzwh:
        for m in find('ypjg315_pingpai',{'批准文号':jddj_pzwh}):
            ypjg315_txm = m.get('条形码')
            ypjg315_gg = m.get('规格')
            ypjg315_name = m.get('原始名称')
            try:
                ypjg315_gg_num = re.findall(pattern,ypjg315_gg)
                # ypjg315_name_num = re.findall(pattern,ypjg315_name)
            except Exception:
                print("ypjg315规格匹配失败",ypjg315_name)
                continue
            try:
                ypjg315_gg_num_list = [float(re.sub('\+','',x)) for x in ypjg315_gg_num if re.sub('\+','',x) and x != '.']
                # ypjg315_name_num_list = [float(re.sub('\+','',x)) for x in ypjg315_name_num if re.sub('\+','',x) and x != '.']
            except Exception:
                print(("ypjg315数字查找失败",ypjg315_gg_num))
                continue

            # if compare(jddj_gg_num_list,ypjg315_gg_num_list) or compare(jddj_name_num_list,ypjg315_name_num_list):
            if compare(jddj_gg_num_list, ypjg315_gg_num_list):
                jddj_content['upcCode'] = str(ypjg315_txm)
                break
            else:
                continue
        try:
            upsert_one('ziying_txm', jddj_content)
        except Exception:
            print(traceback.format_exc())
    else:
        for m in find('ypjg315_pingpai', {'产品名称': jddj_tym,'生产厂家':jddj_pp}):
            ypjg315_txm = m.get('条形码')
            ypjg315_gg = m.get('规格')
            ypjg315_name = m.get('原始名称')
            try:
                ypjg315_gg_num = re.findall(pattern, ypjg315_gg)
                # ypjg315_name_num = re.findall(pattern, ypjg315_name)
            except Exception:
                print("ypjg315规格匹配失败", ypjg315_name)
                continue
            try:
                ypjg315_gg_num_list = [float(re.sub('\+', '', x)) for x in ypjg315_gg_num if
                                       re.sub('\+', '', x) and x != '.']
                # ypjg315_name_num_list = [float(re.sub('\+', '', x)) for x in ypjg315_name_num if
                #                          re.sub('\+', '', x) and x != '.']
            except Exception:
                print("ypjg315数字查找失败", ypjg315_gg_num)
                continue

            if compare(jddj_gg_num_list, ypjg315_gg_num_list):
                jddj_content['upcCode'] = str(ypjg315_txm)
                break
            else:
                continue
        try:
            upsert_one('ziying_txm', jddj_content)
        except Exception:
            print(traceback.format_exc())

