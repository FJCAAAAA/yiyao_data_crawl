#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : ForMedDatebase.py
@Author: Fengjicheng
@Date  : 2020/1/7
@Desc  : 从mongodb中查询获取自定义格式数据
'''
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def data_process(data):
    drugInfo = data.get('drugInfo')
    drugDesc = data.get('drugDesc')
    required_fields = {'drugId': data.get('drugId'),
                       '通用名称': drugInfo.get('drugName'), '规格': drugInfo.get('standard'), '69码': drugInfo.get('barCode'),
                       '功能主治': drugDesc.get('majorFunction'), '成分': drugDesc.get('drugElement'),
                       '性状': drugDesc.get('drugTrait'), '用法用量': drugDesc.get('usageAndDosage'),
                       '不良反应': drugDesc.get('drugAdr'), '禁忌': drugDesc.get('drugTaboo'),
                       '注意事项': drugDesc.get('drugAttention'), '贮藏': drugDesc.get('drugStore'),
                       '包装': drugInfo.get('packageNorm'), '批准文号': drugInfo.get('approvalNumber'),
                       '生产厂家': drugInfo.get('prodCorpName')}
    return required_fields


def all_data_process():
    num = 0
    food_list = find('jyt', {})
    for food in food_list:
        num += 1
        if num > 0:  # 从新的位置开始，如果第一次执行需要置为0
            try:
                data_detail = data_process(food)
                if isinstance(data_detail, dict) and data_detail:
                    insert('jyt_for_meddatebase', data_detail)
            except Exception:
                print('第 {} 个 查询失败'.format(num))
                print(traceback.format_exc())
                continue
    food_list.close()

if __name__ == '__main__':
    all_data_process()


