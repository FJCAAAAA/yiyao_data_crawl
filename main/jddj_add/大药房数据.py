#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : 大药房数据.py
@Author: Fengjicheng
@Date  : 2019/10/9
@Desc  :
'''

from ast import literal_eval
import re
import time
import json
import traceback
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

with open('dayaofang.txt','r',encoding='utf-8') as f:
    content = f.readline()

pattern1 = '{.*?}'
pattern2 = '\\'
spe1 = re.compile(pattern1)
content_list = spe1.findall(content)


for i in tqdm(content_list):
    try:
        insert('dayaofang',json.loads(i.replace(pattern2,'')))
    except Exception:
        print(traceback.format_exc())
        continue
