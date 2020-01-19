#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : for_yaojisong.py
@Author: Fengjicheng
@Date  : 2019/12/30
@Desc  : 查询 elem_food_by_cate 表，获取可用数据
        1.manual为空的，判断illustration是否为空
        
'''
import re
import traceback
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

def data_process(data):
    required_fields = {'商品名称': '', '品牌': '', '通用名称': '', '规格': '', '批准文号': '', '69码': '',
                       '成份': '', '贮藏': '', '包装': '', '剂型': '',
                       '商品图片': '', '处方分类': '', '内服/外用': '', '适合人群': '', '功能主治': '', '性状': '',
                       '用法用量': '', '不良反应': '', '禁忌': '', '注意事项': '', '药物相互作用': '', '有效期': '',
                       '生产企业': ''}
    required_fields['商品名称'] = data.get('upc_name')
    required_fields['品牌'] = data.get('brand_name')
    required_fields['69码'] = data.get('upc')
    required_fields['商品图片'] = data.get('photos')
    manual = data.get('manual')
    if manual:
        required_fields['通用名称'] = manual.get('generic_name')
        required_fields['规格'] = manual.get('specification')
        required_fields['批准文号'] = manual.get('approval_number')
        required_fields['成份'] = manual.get('ingredients')
        required_fields['贮藏'] = manual.get('storage')
        required_fields['包装'] = manual.get('package')
        required_fields['剂型'] = manual.get('dosage_form')
        required_fields['处方分类'] = manual.get('prescription_type_name')
        required_fields['内服/外用'] = manual.get('taking_type_name')
        required_fields['适合人群'] = manual.get('application_type_name')
        required_fields['功能主治'] = manual.get('purpose')
        required_fields['性状'] = manual.get('drug_description')
        required_fields['用法用量'] = manual.get('dosage_administration')
        required_fields['不良反应'] = manual.get('adverse_reactions')
        required_fields['禁忌'] = manual.get('contraindications')
        required_fields['注意事项'] = manual.get('precautions')
        required_fields['药物相互作用'] = manual.get('drug_interactions')
        required_fields['有效期'] = manual.get('validity_period')
        required_fields['生产企业'] = manual.get('production_enterprise')
    else:
        pattern1 = re.compile('【(.*?)】')
        pattern2 = re.compile('\\s')
        illustration_list = data.get('illustration')
        for illustration in illustration_list:
            kv = illustration.get('value')
            k = pattern1.findall(kv)
            if k:
                v = pattern1.sub('', kv)
                required_fields[pattern2.sub('', k[0])] = v.strip()
    return required_fields


def all_data_process():
    num = 0
    food_list = find('elem_food_by_cate', {})
    for food in food_list:
        num += 1
        if num > 0:  # 从新的位置开始，如果第一次执行需要置为0
            try:
                data_detail = data_process(food)
                if isinstance(data_detail, dict) and data_detail:
                    insert('elem_for_yaojisong', data_detail)
            except Exception:
                print('第 {} 个 查询失败'.format(num))
                print(traceback.format_exc())
                continue
    food_list.close()

if __name__ == '__main__':
    all_data_process()
