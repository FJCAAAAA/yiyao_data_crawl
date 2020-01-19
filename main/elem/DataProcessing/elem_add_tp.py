#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : elem_add_tp.py.py
@Author: Fengjicheng
@Date  : 2020/1/7
@Desc  : 饿了么数据添加图片链接字段
'''
import re
import json
from tqdm import tqdm
import time
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class GetTpUri(object):
    def __init__(self):
        self.uri_file = 'upload_file.txt'
        self.img_file = 'img.txt'

    def get_upc_tp_relate(self):
        with open(self.uri_file,'r',encoding='utf-8') as f:
            content_list = f.readlines()
        file = open(self.img_file,'a',encoding='utf-8')
        pattern1 = '(.*)_1.'
        for n in tqdm(content_list):
            n_list = re.split(' ',n)
            sid = n_list[0].strip()
            uri = n_list[1].strip()
            sid_list = re.split('_', sid)
            if re.match(pattern1,sid):
                upc = re.split('/', sid_list[0])[-1]
                file.write('\n' + upc + ' ' + uri)
            else:
                file.write(' ' + uri)
            file.flush()
        file.close()

    def elem_add(self):
        with open(self.img_file,'r',encoding='utf-8') as f:
            content_list = f.readlines()
        for n in tqdm(content_list):
            relate_list = re.split(' ', n.strip())
            food_list = find('elem_for_yaojisong', {'69码': relate_list[0]})
            for food in food_list:
                food['img'] = ','.join(relate_list[1:])
                upsert_one('elem_for_yaojisong', food)
            food_list.close()

if __name__ == '__main__':
    obj = GetTpUri()
    # obj.get_upc_tp_relate()
    obj.elem_add()
