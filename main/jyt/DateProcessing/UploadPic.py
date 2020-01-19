#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : UploadPic.py
@Author: Fengjicheng
@Date  : 2020/1/14
@Desc  : 上传京药通图片，添加链接到批量建品数据
'''
import time
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *
from yiyao_data_crawl.main.common.UploadPicture import *


def jyt_upload_pic():
    jyt = find('jyt_for_meddatebase', {})
    for med in jyt:
        upc = med.get('drugId')
        img_list = []
        for i in range(7):
            path = 'E:/爬虫项目/京药通/picture/' + upc + '_' + str(i) + '.jpg'
            try:
                img_list.append(uploadimg(path))
            except Exception:
                print('{} 上传失败'.format(path))
                continue
        med['img'] = ','.join(img_list)
        upsert_one('jyt_for_meddatebase', med)
    print('jyt 图片上传完成')
    jyt.close()


def jyt_for_pljp():
    pljp = find('jyt_for_pljp', {})
    for med in pljp:
        upc = str(med.get('69码'))
        jyt = find('jyt_for_meddatebase', {'69码': upc})
        for i in jyt:
            med['img'] = i.get('img')
        upsert_one('jyt_for_pljp', med)
    print('jyt_for_pljp 图片链接添加完成')
    pljp.close()

if __name__ == '__main__':
    # jyt_upload_pic()
    jyt_for_pljp()
