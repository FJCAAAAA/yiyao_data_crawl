#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetArea.py
@Author: Fengjicheng
@Date  : 2020/3/5
@Desc  : 获取一级行政区和二级行政区
'''
import requests
import urllib3
import json
import time


class GetArea(object):
    def __init__(self):
        self.first_area_file = 'txt/first_area.txt'
        self.sec_area_file = 'txt/sec_area.txt'
        self.header = {
            'Host': 'www.guahao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'close',
            'Referer': 'https://www.guahao.com/expert/fastorder'
        }
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_first_area(self):
        url = 'https://www.guahao.com/json/white/area/provinces'
        response = requests.get(url=url, headers=self.header, timeout=(10, 10))
        file = open(self.first_area_file, 'a', encoding='utf-8')
        for first_area in response.json():
            first_area_dict = {'一级行政区名称': first_area.get('text'), '一级行政区ID': first_area.get('value')}
            file.write(json.dumps(first_area_dict, ensure_ascii=False) + '\n')
            # print(first_area.get('text'),first_area.get('value'))
        file.close()

    def get_sec_area(self):
        first_area_file = open(self.first_area_file, 'r', encoding='utf-8')
        sec_area_file = open(self.sec_area_file, 'a', encoding='utf-8')
        for first_area in first_area_file:
            first_area_dict = json.loads(first_area)
            first_area_name = first_area_dict.get('一级行政区名称')
            first_area_id = first_area_dict.get('一级行政区ID')
            url = 'https://www.guahao.com/json/white/area/citys?provinceId={}'.format(first_area_id)
            response = requests.get(url=url, headers=self.header, timeout=(10, 10))
            for sec_area in response.json():
                sec_area_dict = first_area_dict.copy()
                sec_area_name = sec_area.get('text')
                sec_area_id = sec_area.get('value')
                if sec_area_name != '不限':
                    sec_area_dict['二级行政区名称'] = sec_area_name
                    sec_area_dict['二级行政区ID'] = sec_area_id
                    sec_area_file.write(json.dumps(sec_area_dict, ensure_ascii=False) + '\n')
                    sec_area_file.flush()
            print('{} 的 二级行政区 爬取完成'.format(first_area_name))
            time.sleep(1)
        first_area_file.close()
        sec_area_file.close()

if __name__ == '__main__':
    obj = GetArea()
    # obj.get_first_area()
    obj.get_sec_area()