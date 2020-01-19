#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : JsonToCsv.py
@Author: Fengjicheng
@Date  : 2019/12/2
@Desc  : 将json文件格式转为csv文件格式并保存。
'''

import csv
import json
import codecs


class Json_Csv():

    # 初始化方法，创建csv文件。
    def __init__(self, name):
        self.save_csv = open(name, 'w', encoding='utf-8', newline='')
        self.write_csv = csv.writer(self.save_csv, delimiter=',')  # 以，为分隔符

    def trans(self, filename):
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            read = f.readlines()
            flag = True
            for index, info in enumerate(read):
                data = json.loads(info)
                # if index <3000: #读取json文件的前3000行写入csv文件 。要是想写入全部，则去掉判断。
                if flag:  # 截断第一行当做head
                    keys = list(data.keys())  # 将得到的keys用列表的形式封装好，才能写入csv
                    self.write_csv.writerow(keys)
                    flag = False  # 释放
                value = list(data.values())   # 写入values，也要是列表形式
                self.write_csv.writerow(value)
            self.save_csv.close()  # 写完就关闭

# obj = Json_Csv('E:\爬虫项目\中文医学知识图谱\实体及类型表_last.csv')
# obj.trans('D:\project\yiyao_data_crawl\yiyao_data_crawl\main\cmekg\data_change\实体及类型表.json')

obj = Json_Csv('E:\爬虫项目\中文医学知识图谱\关系表_last.csv')
obj.trans('D:\project\yiyao_data_crawl\yiyao_data_crawl\main\cmekg\data_change\关系表.json')