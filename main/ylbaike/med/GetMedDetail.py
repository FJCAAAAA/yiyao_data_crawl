#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetMedDetail.py
@Author: Fengjicheng
@Date  : 2019/12/9
@Desc  : 百度百科药物详情爬取
'''
import re
import random
import urllib3
import json
import time
import requests
import traceback
from bs4 import BeautifulSoup
from lxml import etree
from tqdm import tqdm
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

class GetMed(object):
    def __init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.spe1 = '。，：；．.,:;'
        self.pattern1 = re.compile('：')
        self.pattern2 = re.compile('、')
        self.pattern3 = re.compile('。')
        self.pattern4 = re.compile('^[^0-9].*：$')  #匹配概括性语句，例如 "阿莫西林适用于敏感菌(不产β内酰胺酶菌株)所致的下列感染："
        self.pattern5 = re.compile('^[0-9]+(\.|．).*')  #匹配数字开头的语句，例如 "2.大肠埃希菌、奇异变形杆菌或粪肠球菌所致的泌尿生殖道感染。"
        self.pattern6 = re.compile('[0-9]+(\.|．)')

    def get_response_content(self, url):
        header = {
            'Host': 'baike.baidu.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://baike.baidu.com/wikitag/taglist?tagId=75954',
            'Connection': 'close',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        num = 0
        while True:
            num += 1
            if num > 5:
                print('请求失败%s次，请手动检查 %s' % (num, url))
                return False

            response = requests.get(url, headers=header, timeout=(5, 5), verify=False)
            if response.status_code == 200:
                html = response.content.decode('utf-8')
                return html
            else:
                print('请求失败%s次' % (num))

    def large_text(self, obj):
        if type(obj) == list and len(obj) != 0:
            # 判断首行是否是概括性语句,如果是，就排除掉
            if self.pattern4.match(obj[0]):
                obj = obj[1:]
            # 判断格式是否数字开头
            if self.pattern5.match(obj[0]):
                obj_new = self.pattern6.split(''.join(obj))
            else:
                obj_new = obj
            return [x.strip(self.spe1) for x in obj_new if
                    x.strip(self.spe1) != '' and x.strip(self.spe1) != '，' and x.strip(self.spe1) != '、']
        else:
            return ''

    def get_one_page(self, name, url):
        data = {
            '药物名称': '', '药品简介': '', '药品类型': '', '药品类型（作用类别）': '',
            '用途分类': '', '成份': '', '性状': '', '适应症': '', '规格': '', '用法用量': '', '不良反应': '',
            '禁忌': '', '注意事项': '', '孕妇及哺乳期妇女用药': '', '儿童用药': '', '老年用药': '',
            '药物相互作用': '', '药物过量': '', '药理毒理': '', '药理作用': '', '药理毒理（药理作用）': '',
            '药代动力学': '', '贮藏': '', '包装': '', '有效期': '', '执行标准': '', '功能主治': '',
            '警示语': '', '相互作用': '', '数据来源': ['百度百科'], '爬取时间': '%s' % (time.strftime("%Y-%m-%d", time.localtime()))
        }
        data['药物名称'] = name  # 药物名称 字段
        html = self.get_response_content(url)
        soup = (BeautifulSoup(html, 'lxml') if html else False)
        # 判断主体末端是哪种标签
        if soup.find('div', class_='tashuo-bottom'):
            sep0 = '<div class="tashuo-bottom" id="tashuo_bottom">'
        elif soup.find('dt', class_='reference-title'):
            sep0 = '<dt class="reference-title">'
        elif soup.find('div', class_='lemma-paper-box'):
            sep0 = '<div class="lemma-paper-box">'
        elif soup.find('div', class_='open-tag-title'):
            sep0 = '<div class="open-tag-title">'
        html = re.split(sep0, html)[0]
        soup = BeautifulSoup(html, 'lxml')
        summary = soup.find('div', class_='lemma-summary').get_text().strip()
        data['药品简介'] = summary  # 药品简介 字段
        main_tab = soup.find('div', class_='main-content')
        if not main_tab:
            main_tab = soup.find('div', class_='main_tab main_tab-defaultTab curTab')
        base_info = main_tab.find('div', class_='basic-info cmn-clearfix')
        if base_info:  # 判断基本信息是否存在
            dt_detail = base_info.find_all('dt', class_='basicInfo-item name')
            dd_detail = base_info.find_all('dd', class_='basicInfo-item value')
            for dt, dd in zip(dt_detail, dd_detail):
                dt_text = dt.get_text().strip()
                dd_text = dd.get_text().strip()
                if dt_text in ['药品类型', '用途分类']:
                    dd_text_list = re.split('、', dd_text)
                    data[dt_text] = dd_text_list
            yplx = data.get('药品类型')
            data['药品类型（作用类别）'] = yplx  # 药品类型（作用类别） 字段
        else:
            print(name, "没有基本信息")
        data.pop('药品类型')
        data_new = data.copy()
        # 正文部分分割处理
        spe1 = '<div class="anchor-list">'
        for i in re.split(spe1, html):
            xhtml = etree.HTML(i)
            # xtitle = xhtml.xpath('//div[@label-module="para-title"]/h2/text()')  # key
            xtitle = xhtml.xpath('//div[@class="para-title level-2"]/h2/text()')  # key
            if xtitle:
                key = xtitle[0].strip()
                value = ''
                value_new = ''
                value_list = xhtml.xpath('//div[@class="para"]/text()')
                value_list = [x.strip() for x in value_list if x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                # if value_list:   ###########
                value_str1 = '\n'.join(value_list)
                # value_str2 = ''.join(value_list)
                if key in data:
                    if key == '成份':
                        for n in value_list:
                            chengfen = re.match('.*化学名称.*：.*', n)
                            if chengfen:
                                value = self.pattern1.split(n)[1:]
                        if not value:
                            value = self.pattern2.split(self.pattern3.split(value_list[0])[0])
                        value = [x.strip(self.spe1) for x in value]
                        value_new = value
                    elif key == '适应症':
                        value = self.large_text(value_list)
                        value_new = value
                    elif key == '规格':
                        value = ''.join(value_list)
                        value_new = value
                    elif key in ['用法用量', '不良反应', '注意事项', '药物相互作用']:
                        value = value_str1
                        value_new = self.large_text(value_list)
                    else:
                        value = value_str1
                        value_new = value_str1
                    data[key] = value
                    data_new[key] = value_new
        yldl = data.get('药理毒理')
        ylzy = data.get('药理作用')
        data['药理毒理（药理作用）'] = (yldl if yldl else ylzy)  # 药理毒理（药理作用） 字段
        data_new['药理毒理（药理作用）'] = (yldl if yldl else ylzy)  # 药理毒理（药理作用） 字段
        data.pop('药理毒理')
        data.pop('药理作用')
        data_new.pop('药理毒理')
        data_new.pop('药理作用')
        insert('bdbk_yw', data)
        insert('bdbk_yw_ycl', data_new)
        # print(json.dumps(data, ensure_ascii=False))
        # print(json.dumps(data_new, ensure_ascii=False))

    def get_all_page(self):
        with open('fail_url.txt', 'r', encoding='utf-8') as f:
            med_list = f.readlines()
        fail_file = open('fail_url.txt', 'a', encoding='utf-8')
        for i in tqdm(med_list):
            a = eval(i.strip('\n'))
            for name, url in a.items():
                try:
                    self.get_one_page(name, url)
                except Exception :
                    fail_file.write(i)
                    fail_file.flush()
                    print(name, url, "爬取失败")
                    print(traceback.format_exc())
            time.sleep(1)
        fail_file.close()


if __name__ == '__main__':
    obj = GetMed()
    obj.get_all_page()
