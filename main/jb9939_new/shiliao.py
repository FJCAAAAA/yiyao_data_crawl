#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : shiliao.py
@Author: Fengjicheng
@Date  : 2019/11/21
@Desc  :
'''
from bs4 import BeautifulSoup
from yiyao_data_crawl.main.common.WebUtils import *

result = {'症状名称': 'name', '症状简介': '', '症状起因': '', '预防': '', '检查': '', '可能疾病信息': [], '相关症状': [],
              '宜吃饮食信息': '', '忌吃饮食信息': '', '宜吃饮食种类': '', '宜吃食物': [], '忌吃饮食种类': '', '忌吃食物': [],
              '就诊科室':[]}

url = 'https://jb.9939.com/zhengzhuang/altk/'
page = url.split('/')[-2] + '_shiliao.html'
with open('9939/%s' % (page), 'r',encoding='utf-8') as f:
    page_ctt = f.read()

sl_soup = BeautifulSoup(page_ctt,'html.parser')
sl_div = sl_soup.find('div',class_='spread')
sl_list = str(sl_div).split('<b>忌吃饮食</b>')

for i in sl_list:
    ys_soup = BeautifulSoup(i,'html.parser')
    zl_soup = ys_soup.find('p')
    sw_soup_list = ys_soup.find_all('p',style=True)

    xx = zl_soup.text
    zl = zl_soup.text
    sw = []

    for sw_soup in sw_soup_list:
        xx += sw_soup.text
        sw.append(re.split('\\s',sw_soup.text)[0].strip())
    if sl_list.index(i) == 0:
        result['宜吃饮食信息'] = xx
        result['宜吃饮食种类'] = zl
        result['宜吃食物'] = sw
    elif sl_list.index(i) == 1:
        result['忌吃饮食信息'] = xx
        result['忌吃饮食种类'] = zl
        result['忌吃食物'] = sw

jzks_div = sl_soup.find('div',class_='third-doc btline mT18')
item_for(result, '就诊科室', jzks_div.find_all('a'), 'list')
print(result)