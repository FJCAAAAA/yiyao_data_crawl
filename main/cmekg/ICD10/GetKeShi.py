#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetKeShi.py
@Author: Fengjicheng
@Date  : 2019/12/2
@Desc  : IDC10科室
'''

import json
from tqdm import tqdm

#查询科室
def get_keshi():
    with open('科室.json', 'r', encoding='utf-8') as f:
        keshi = f.read()
    node_list = json.loads(keshi)['nodes']
    file = open('keshi_sym.txt', 'a', encoding='utf-8')
    for n in tqdm(node_list):
        keshi_dict = {}
        if n['icon'] == '../static/images/datarange.png':
            letter_ke_id = n['pId']
            sym_name = n['name']
            for m in node_list:
                if m['id'] == letter_ke_id:
                    sec_ke_id = m['pId']
                    for x in node_list:
                        if x['id'] == sec_ke_id:
                            sec_ke_name = x['name']
                            first_ke_id = x['pId']
                            for y in node_list:
                                if y['id'] == first_ke_id:
                                    first_ke_name = y['name']
                                    keshi_dict['疾病名称'] = sym_name
                                    keshi_dict['一级科室'] = first_ke_name
                                    keshi_dict['二级科室'] = sec_ke_name
                                    file.write(json.dumps(keshi_dict, ensure_ascii=False) + '\n')
                                    file.flush()


if __name__ == '__main__':
    get_keshi()



