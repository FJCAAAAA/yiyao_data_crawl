#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : CsvToJson.py
@Author: Fengjicheng
@Date  : 2020/2/24
@Desc  :
'''
import csv
import json

def csv_to_json(csv_file, json_file):
    file = open(json_file, 'a', encoding='utf-8')
    with open(csv_file, 'r', encoding='utf-8')as f:
        f_csv = csv.reader(f)
        my_list = []
        for row in f_csv:
            for index in range(len(row)):
                my_list.append(row[index])
            break
        # print(my_list)
        for row in f_csv:
            result_dict = {}
            for index in range(len(row)):
                result_dict[my_list[index]] = row[index]
            file.write(json.dumps(result_dict, ensure_ascii=False) + '\n')
    file.close()

if __name__ == '__main__':
    csv_to_json('D:\工作\数据\主数据\hospital.csv', 'D:\工作\数据\主数据\hospital.json')