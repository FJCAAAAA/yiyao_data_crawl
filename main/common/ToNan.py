#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ToNan.py
@Author: Fengjicheng
@Date  : 2019/12/11
@Desc  : 空字段转换为"NAN"，去除列表中元素开头的序号
'''

import re
import json
from tqdm import tqdm

pattern1 = re.compile(r'([一二三四五六七八九十0-9]+[,.:．，、：]{1})|([\(（]{1}[一二三四五六七八九十0-9]+[\)）]{1})|([①②③④⑤⑥⑦⑧⑨⑩][,.．、，：]?)')
spe1 = '([一二三四五六七八九十0123456789]+[,.:．，、：]{1})|([\(（]{1}[一二三四五六七八九十0-9]+[\)）]{1})|([①②③④⑤⑥⑦⑧⑨⑩][,.．、，：]?)'

def to_nan(filename_old, filename_new):
    with open(filename_old, 'r', encoding='utf-8') as f:
        content_list = f.readlines()
    file = open(filename_new, 'a', encoding='utf-8')
    for line in tqdm(content_list):
        line_dict = json.loads(line)
        line_new = line_dict
        for k, v in line_dict.items():
            if not v:
                line_new[k] = 'NAN'  # 处理空字段
            if v and type(v) == list:
                #v_new = [x.lstrip(spe1).strip() for x in v]
                v_new = [pattern1.sub('', x, count=1).strip() for x in v]
                line_new[k] = v_new
        file.write(json.dumps(line_new, ensure_ascii=False) + '\n')
        file.flush()
    file.close()

# to_nan('百度百科药物数据_原.json', '百度百科药物数据_原_new.json')
# to_nan('百度百科药物数据_预处理.json', '百度百科药物数据_预处理_new.json')
