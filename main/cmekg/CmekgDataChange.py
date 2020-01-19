#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CmekgDataChange.py
@Author: Fengjicheng
@Date  : 2019/12/19
@Desc  :
'''
import json
from tqdm import tqdm


def one_line(data):
    data1 = {'实体名称': '', '实体类型': ''}
    data2 = {'源实体': '', '关系类型': '', '目标实体': ''}
    file1 = open('data_change\实体及类型表.json', 'a', encoding='utf-8')
    file2 = open('data_change\关系表.json', 'a', encoding='utf-8')
    # 处理名称
    data1['实体名称'] = data.get('名称')
    data1['实体类型'] = data.get('类型')
    file1.write(json.dumps(data1, ensure_ascii=False) + '\n')
    file1.flush()
    for k, v in data.items():
        if k not in ['名称', '类型']:
            if type(v) == list:
                for i in v:
                    data1['实体名称'] = i
                    data1['实体类型'] = k
                    file1.write(json.dumps(data1, ensure_ascii=False) + '\n')
                    file1.flush()
                    data2['源实体'] = data.get('名称')
                    data2['关系类型'] = k
                    data2['目标实体'] = i
                    file2.write(json.dumps(data2, ensure_ascii=False) + '\n')
                    file2.flush()

if __name__ == '__main__':
    with open('cmekg_last.json', 'r', encoding='utf-8') as f:
        for i in tqdm(f.readlines()):
            one_line(json.loads(i))
