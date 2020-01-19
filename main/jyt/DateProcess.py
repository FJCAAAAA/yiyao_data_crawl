#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : DateProcess.py
@Author: Fengjicheng
@Date  : 2020/1/6
@Desc  : 京药通App 药品数据处理
'''
import json
import traceback
from GetJingyaotong import RequestJingYaoTong
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class DateProJingYaoTong(object):
    def __init__(self):
        self.request_obj = RequestJingYaoTong()
        self.cate_list = json.loads(self.request_obj.get_med_cate())

    def get_all_drugId(self):
        '''
        循环爬取所有的drugId
        :return: 
        '''
        for cate in self.cate_list:
            paraValue = cate.get('paraValue')
            name = cate.get('name')
            if paraValue != 'YPYTFL':
                pageIndex = 0
                while True:
                    pageIndex += 1
                    print('开始爬取 {} 第 {} 页的drugId'.format(name, pageIndex))
                    try:
                        med_dict = json.loads(self.request_obj.get_med_list(paraValue, pageIndex))
                    except Exception:
                        print(traceback.format_exc())
                        continue
                    med_list = med_dict.get('data').get('data')
                    if not med_list:
                        break
                    for med in med_list:
                        drugId = med.get('id')
                        insert('jyt', {'类目': name, 'drugId': drugId})

    def get_all_med_detail(self):
        '''
        循环爬取所有药品详情
        :return: 
        '''
        drugId_list = find('jyt', {})
        for drugId_dict in drugId_list:
            drugId = drugId_dict.get('drugId')
            print('开始爬取 {} 的药品详情'.format(drugId))
            med_detail = json.loads(self.request_obj.get_med_detail(drugId))
            if isinstance(med_detail, dict) and med_detail.get('data'):
                drugId_dict['drugDesc'] = med_detail.get('data').get('drugDesc')
                drugId_dict['drugInfo'] = med_detail.get('data').get('drugInfo')
                drugId_dict['ypPics'] = med_detail.get('data').get('ypPics')
                upsert_one('jyt', drugId_dict)
        drugId_list.close()

    def get_all_med_pic(self):
        '''
        循环爬取所有药品图片
        :return: 
        '''
        num = 0
        drugId_list = find('jyt', {})
        for drugId_dict in drugId_list:
            num += 1
            if num < 4780:
                continue
            drugId = drugId_dict.get('drugId')
            print('开始爬取 {} 的图片，num：{}'.format(drugId, num))
            pic_list = drugId_dict.get('ypPics')
            if pic_list:
                for route in pic_list:
                    try:
                        pic_content = self.request_obj.get_picture(route)
                        path = 'E:/爬虫项目/京药通/picture/' + drugId + '_' + str(pic_list.index(route)) + '.jpg'
                        with open(path, 'wb') as f:
                            f.write(pic_content)
                    except Exception:
                        print(traceback.format_exc())
                        continue
        drugId_list.close()


if __name__ == '__main__':
    obj = DateProJingYaoTong()
    # obj.get_all_drugId()
    # obj.get_all_med_detail()
    obj.get_all_med_pic()
