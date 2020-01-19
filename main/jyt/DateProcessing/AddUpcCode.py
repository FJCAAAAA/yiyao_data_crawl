#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AddUpcCode.py
@Author: Fengjicheng
@Date  : 2020/1/8
@Desc  : 
'''
import time
from tqdm import tqdm
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *
from yiyao_data_crawl.main.common.OCRByBaidu import *


def jyt_add_upc():
    num = 0
    picture_dir = 'E:/爬虫项目/京药通/picture/'
    food_list = find('jyt_for_meddatebase_bak', {"69码": None})
    file = open('ocr_226.txt', 'a', encoding='utf-8')
    for food in food_list:
        num += 1
        if num in range(226, 300):
            drugId = food.get('drugId')
            print('第 {} 个 ，drugId：{}'.format(num, drugId))
            for index in range(0, 7):
                path = picture_dir + drugId + '_{}.jpg'.format(index)
                file.write(drugId + ' ' + get_upc(path) + '\n')
                file.flush()
                time.sleep(1)
    file.close()


if __name__ == '__main__':
    jyt_add_upc()