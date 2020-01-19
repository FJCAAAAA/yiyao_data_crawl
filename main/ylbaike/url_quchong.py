#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_jibing_detail.py
@Author: Fengjicheng
@Date  : 2019/8/11
@Desc  :
'''
def url_quchong(file_url_name,file_uniq_url_name):
    with open(file_url_name,'r',encoding='utf-8') as f:
        urllist = set(f.readlines())
    print(len(urllist))
    with open(file_uniq_url_name,'a',encoding='utf-8') as n:
        for i in urllist:
            n.write(i)

# url_quchong('jibing_url.txt','jibing_url_uniq.txt')
url_quchong('med/yaowu_url.txt','med/yaowu_url_uniq.txt')