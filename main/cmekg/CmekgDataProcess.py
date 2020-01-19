#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CmekgDataProcess.py
@Author: Fengjicheng
@Date  : 2019/11/29
@Desc  : 中文医学知识图谱数据处理，并写入mongodb
'''

import requests
import json
import random
import time
import traceback
from tqdm import tqdm
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_one_url(url):
    header = {
        'Host': 'zstp.pcl.ac.cn:8002',
        'User-Agent': random.choice(pcUserAgent),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    num = 0
    while True:
        graph_dict = {}
        num += 1
        response = requests.get(url, headers=header, timeout=(5, 5))
        content = response.content.decode('utf-8')
        if num > 5:
            break
        if response:
            # 数据处理
            content_dict = json.loads(content)
            graph_dict['名称'] = content_dict.get('name')
            graph_dict['类型'] = content_dict.get('tree_type')
            cate_list = content_dict.get('categories')
            node_list = content_dict.get('node')
            for index, info in enumerate(cate_list):
                if index > 1:
                    cate = info['name']
                    cate_node = []
                    for node in node_list:
                        if node['category'] == index:
                            cate_node.append(node['label'])
                    graph_dict[cate] = cate_node
            # print('{} 请求成功'.format(graph_dict.get('名称')))
            return graph_dict
        else:
            print('请求失败%s，1秒后再次请求' % (url))
            print(content)
            time.sleep(1)


def get_all_url():
    for k, v in {'疾病.txt': '疾病', '症状.txt': '症状', '药物分类.txt': '药物分类', '检查诊疗技术.txt': '检查诊疗技术'}.items():
        print('**********正在爬取 {} 信息**********'.format(v))
        with open(k, 'r', encoding='utf-8') as f:
            content_list = f.readlines()
        for name in tqdm(content_list):
            try:
                url = 'http://zstp.pcl.ac.cn:8002/knowledge?name=%s&tree_type=%s' % (name.strip(), v)
                insert('cmekg_tupu', get_one_url(url))
            except Exception:
                print('{} 爬取失败'.format(name))
                print(print(traceback.format_exc()))
                continue
# def get_all_url():
#     for k, v in {'感冒': '疾病'}.items():
#         # print('**********正在爬取 {} 信息**********'.format(v))
#         # with open(k, 'r', encoding='utf-8') as f:
#         #     content_list = f.readlines()
#         # for name in tqdm(content_list):
#         try:
#             url = 'http://zstp.pcl.ac.cn:8002/knowledge?name=%s&tree_type=%s' % (k.strip(), v)
#             insert('cmekg_tupu_last', get_one_url(url))
#         except Exception:
#             print('{} 爬取失败'.format(k))
#             print(print(traceback.format_exc()))
#             continue


if __name__ == '__main__':
    get_all_url()
