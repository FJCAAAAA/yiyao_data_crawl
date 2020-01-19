#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ICD10_add_keshi.py
@Author: Fengjicheng
@Date  : 2019/12/2
@Desc  : ICD10疾病添加科室字段
'''

import time
import json
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

with open('ICD10.txt','r',encoding='utf-8') as f:
    ICD10_list = f.readlines()

with open('keshi.txt','r',encoding='utf-8') as f:
    keshi_sym_list = f.readlines()
file_no = open('ICD10NoKeshi.json','a',encoding='utf-8')
file = open('ICD10AndKeshi.json','a',encoding='utf-8')
for n in tqdm(ICD10_list):
    ICD10 = json.loads(n)
    ICD10_sym_name = ICD10['疾病名称']
    for m in keshi_sym_list:
        keshi_sym = json.loads(m)
        if keshi_sym['疾病名称'] == ICD10_sym_name:
            ICD10['一级科室'] = keshi_sym['一级科室']
            ICD10['二级科室'] = keshi_sym['二级科室']
            # file.write(json.dumps(ICD10,ensure_ascii=False) + '\n')
            # file.flush()
    if not ICD10.get('一级科室'):
        file_no.write(json.dumps(ICD10,ensure_ascii=False) + '\n')
        file_no.flush()

            # insert('ICD10',ICD10)
    # print(ICD10)
    # print(ICD10_sym_name)
    # time.sleep(5)

