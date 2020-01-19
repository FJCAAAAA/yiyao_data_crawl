#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : jddj_add_tp.py
@Author: Fengjicheng
@Date  : 2019/10/18
@Desc  :
'''

import re
import json
from tqdm import tqdm
import time
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class GetTpUri(object):
    def __init__(self):
        self.uri_file = 'picture_upload.txt'
        self.img_file = 'img.txt'

    def upsert_mongodb(self):
        with open(self.uri_file,'r',encoding='utf-8') as f:
            content_list = f.readlines()
        for n in tqdm(content_list):
            n_list = re.split(' ',n)
            sid = n_list[0].strip()
            uri = n_list[1].strip()
            sid_list = re.split('_',sid)
            oid = "ObjectId(%s)" %(sid_list[0])
            img_name = re.split('\.',"img_%s" %(sid_list[1]))[0]
            upsert_one('jddj_img',{'_id':oid,img_name:uri})
            # print(type({'_id':oid,img_name:uri}))
            # time.sleep(10)


    def upsert_file(self):
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
                file.write('\n' + sid_list[0] + ' ' + uri)
            else:
                file.write(' ' + uri)
            file.flush()
        file.close()


    def upsert_mongodb1(self):
        with open(self.img_file,'r',encoding='utf-8') as f:
            content_list = f.readlines()
        for n in tqdm(content_list):
            n_list = re.split(' ',n)
            oid = "ObjectId(%s)" %(n_list[0])
            uri_list = [x.strip() for x in n_list[1:]]
            # print({'_id':oid,'img':uri_list})
            insert('jddj_img1',{'_id':oid,'img':uri_list})


obj = GetTpUri()
# obj.upsert_mongodb()
# obj.upsert_file()
obj.upsert_mongodb1()
