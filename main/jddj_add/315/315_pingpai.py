#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : 315_pingpai.py
@Author: Fengjicheng
@Date  : 2019/10/28
@Desc  :315数据添加品牌字段
'''

import re
import json
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

pattern1 = re.compile('\((.*?)\)')

with open('ypjg315.json','r',encoding='utf-8') as f:
    ypjg315 = f.readlines()

for n in tqdm(ypjg315):
    ypjg315_dict = json.loads(n.strip())
    ypjg315_dict.pop("_id")
    ypjg315_name = ypjg315_dict.get('原始名称')
    ypjg315_pingpai_list = pattern1.findall(str(ypjg315_name))
    if ypjg315_pingpai_list:
        ypjg315_pingpai = ypjg315_pingpai_list[-1]
        ypjg315_dict['品牌名称'] = ypjg315_pingpai
        insert('ypjg315_pingpai',ypjg315_dict)
        # print(ypjg315_dict)
        # time.sleep(5)
    else:
        insert('ypjg315_pingpai',ypjg315_dict)
        # print(ypjg315_dict)
        # time.sleep(5)

