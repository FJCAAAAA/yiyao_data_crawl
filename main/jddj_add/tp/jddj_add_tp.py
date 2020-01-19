#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_tp.py.py
@Author: Fengjicheng
@Date  : 2019/10/21
@Desc  :
'''

import time
import json
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

pattern1 = re.compile('\[|\]')

with open('jddj_quan_upcCode.json','r',encoding='utf-8') as f:
    content = f.readlines()

for i in tqdm(content):
    # print(i)
    jddj_content = json.loads(i.strip())
    oid = jddj_content.get('_id')
    for n in find('jddj_img1',{'_id':oid}):
        img_list = n['img']
        jddj_content['img'] = re.sub(pattern1,'',str(img_list))
    upsert_one('jddj_quan',jddj_content)
    # time.sleep(10)