#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CmekgGetUrl.py
@Author: Fengjicheng
@Date  : 2019/11/29
@Desc  : 从json文件获取所有node的名称，并写入txt文件
'''

import json
from tqdm import tqdm


def get_name(filename_r,filename_w):
    with open(filename_r, 'r', encoding='utf-8') as f:
        content = f.read()
    content = json.loads(content)
    nodes = content['nodes']
    file = open(filename_w, 'a', encoding='utf-8')
    for n in tqdm(nodes):
        if n['icon'] == '../static/images/datarange.png':
            name = n['name']
            file.write(name + '\n')
            file.flush()
    file.close()

if __name__ == '__main__':
    try:
        for k, v in {'疾病.json': '疾病.txt', '症状.json': '症状.txt', '药物.json': '药物分类.txt', '诊疗.json': '检查诊疗技术.txt'}.items():
            print('----------------------开始处理%s----------------------' % (k))
            get_name(k,v)
            print('----------------------结束处理%s----------------------' % (k))
    except Exception as e:
        print(e)
