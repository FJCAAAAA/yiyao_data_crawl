#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetICD10Sym.py
@Author: Fengjicheng
@Date  : 2019/12/2
@Desc  : ICD10疾病名称和编码
'''

import json
import re
from tqdm import tqdm

with open('ICD10.json','r',encoding='utf-8') as f:
    content = f.read()
content = json.loads(content)
nodes = content['nodes']

file = open('ICD10_sym.txt','a',encoding='utf-8')

for n in tqdm(nodes):
    sym = {}
    if n['icon'] == '../static/images/datarange.png':
        sym_name= n['name']
        sym_pid = n['pId']
        for m in nodes:
            if m['id'] == sym_pid:
                sym_bianma_name = m['name']
                sym_bianma = re.split(' ',sym_bianma_name)[0].strip()
                sym['ICD10编码'] = sym_bianma
                sym['疾病名称'] = sym_name
                file.write(json.dumps(sym,ensure_ascii=False) + '\n')
                file.flush()



