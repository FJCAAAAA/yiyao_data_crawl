#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : pop_id.py
@Author: Fengjicheng
@Date  : 2019/11/25
@Desc  : mongodb 导出的json文件去除id字段
'''

import json
import re
from tqdm import tqdm

def mongofile_pop_id(filename):
    with open(filename,'r',encoding='utf-8') as f:
        content_list = f.readlines()
    filename_list = re.split('\.',filename)
    new_filename = filename_list[0] + '_new.' + filename_list[1]
    new_file = open(new_filename,'a',encoding='utf-8')
    for line in tqdm(content_list):
        line_dict = json.loads(line)
        line_dict.pop('_id')
        line_str = json.dumps(line_dict,ensure_ascii=False)
        new_file.write(line_str + '\n')
        new_file.flush()
    new_file.close()

mongofile_pop_id('cmekg_原.json')
