#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : elem_add_pp.py
@Author: Fengjicheng
@Date  : 2020/1/2
@Desc  : 饿了么添加品牌ID
'''
import json
import re
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def elem_add_ppid():
    pattern1 = re.compile(' ')
    pattern2 = re.compile('（.*?）|（.*')

    with open('D:\project\yiyao_data_crawl\yiyao_data_crawl\main\jddj_add\quan\jddj_pingpai_uniq.json','r',encoding='utf-8') as f:
        Pingpai = f.readlines()

    for n in tqdm(Pingpai):
        PingpaiDict = json.loads(n.strip())
        PingpaiName = str(PingpaiDict.get('品牌名称'))
        PingpaiNameX = re.sub(pattern2,'',str(PingpaiName))
        PingpaiId = PingpaiDict.get('品牌id')
        for m in find('elem_for_yaojisong', {'品牌': PingpaiNameX}):
            m['品牌ID'] = PingpaiId
            upsert_one('elem_for_yaojisong', m)
        # print(PingpaiNameX)

if __name__ == '__main__':
    elem_add_ppid()
