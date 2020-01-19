#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : SearchDisQa.py
@Author: Fengjicheng
@Date  : 2020/1/8
@Desc  : 寻医问药 疾病提问 数据爬取
'''
import random
import re
from yiyao_data_crawl.main.common.UserAgent import *
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class XunyiwenyaoQa(object):
    def __init__(self):
        self.api = 'http://so.xywy.com/comse.php'
        self.api_1 = 'http://so.xywy.com/comse.php?keyword=%E6%84%9F%E5%86%92&page=1&src=so'

    def search(self, keyword, page):
        data = {
            'keyword': keyword,
            'page': str(page),
            'src': 'so'
        }
        header = {
            'Host': 'so.xywy.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'close',
            'Cache-Control': 'max-age=0',
            # 'Cookie': 'cookie_user_temporary=39325299; clientac=1577688983248749081; visit_dt=2019-11-30; tj_lastUrl=http%3A//so.xywy.com/%3Fsrc%3Dso; tj_lastUrl_time=1578553869703; XYWYDATAxywy=1577688983-1894173069@157768898325329322644389@154; countNum=126; searchRecord=%E6%89%81%E6%A1%83%E4%BD%93%E5%91%A8%E5%9B%B4%E8%84%93%E8%82%BF%20%E5%A4%B4%E6%99%95|%E6%89%81%E6%A1%83%E4%BD%93%E5%91%A8%E5%9B%B4%E8%84%93%E8%82%BF%20%E5%92%BD%E5%B9%B2%7C%E6%84%9F%E5%86%92%20%E5%A4%B4%E7%97%9B%7C%E6%84%9F%E5%86%92; delNum=0; Hm_lvt_f954228be9b5d93a74a625d18203e150=1578295594; UM_distinctid=16f79bf923fd8-07d4974968d1db8-4c302a7b-1fa400-16f79bf924046c; __ads_session=hxMs33KuaAkzm1A6LwA=; ajsDataSession=157854987339511342@12@1578553869@1@http%253A%252F%252Fso.xywy.com%252F%253Fsrc%253Dso@; XYWYDATASESSIONxywy=15785498733991361221@12@1578553869@1@http%253A%252F%252Fso.xywy.com%252F%253Fsrc%253Dso@; city=%B1%B1%BE%A9%CA%D0; __gg_t_city=%B1%B1%BE%A9%CA%D0; __gg_t_loc=%B1%B1%BE%A9%CA%D0; city_xywy_ad=åäº¬å¸; __gg_city=åäº¬å¸; beijing=true; Hm_lpvt_f954228be9b5d93a74a625d18203e150=1578539718; XYWYDATADAYxywy=1578532147-1578585600@17',
            'Referer': 'http://so.xywy.com/?src=so',
            'Upgrade-Insecure-Requests': '1'
        }
        soup = get_soup(self.api, 0, header, 'utf-8', data)
        # print(soup)
        result = soup.find_all('a', class_='comse-result')
        qa_list = [x.get('href') for x in result if x]
        if page == 1:
            pattern1 = re.compile('.*&page=(.*?)&src=so')
            page_last_soup = soup.find('a', attrs={"onmousedown": "__svcl(this, 't=pageChange&p=9&w=尾页')"})
            if page_last_soup:
                page_last = page_last_soup.get('href')
                page_num_list = pattern1.findall(page_last)
                # if len(page_num_list) == 1:
                page_num = page_num_list[0]
            else:
                page_num = '50'
            return [qa_list, page_num]
        else:
            return [qa_list]

    # @staticmethod
    def get_all_qa_url(self, keyword):
        file = open('qa_url.txt', 'a', encoding='utf-8')
        page_num = int(self.search(keyword, 1)[1])
        qa_list = []
        for num in range(1, page_num+1):
            try:
                print('开始查找 {} 的 第 {} 页 的 qa_url'.format(keyword, num))
                qa_list += self.search(keyword, num)[0]
                # time.sleep(0.5)
            except Exception:
                print(traceback.format_exc())
                continue
        file.write(':'.join([keyword, str(qa_list)]) + '\n')
        file.close()
        return qa_list

    def get_all_qa(self, keyword):
        header = {
            'Host': 'club.xywy.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        qa_list = self.get_all_qa_url(keyword)
        if qa_list:
            for url in qa_list:
                try:
                    print('关键字：{} url：{}'.format(keyword, url))
                    soup = get_soup(url, 0, header, 'gbk')
                    qa_text = soup.find('div', attrs={'id': 'qdetailc'}).get_text()
                    qa_text = re.sub('\\s', '', qa_text)
                    insert('xywy', {'关键字': keyword, '提问': qa_text})
                    # time.sleep(0.5)
                except Exception:
                    print(traceback.format_exc())
                    continue

if __name__ == '__main__':
    obj = XunyiwenyaoQa()
    # print(obj.get_all_qa_url('感冒'))
    obj.get_all_qa('扁桃体周围脓肿 头晕')

