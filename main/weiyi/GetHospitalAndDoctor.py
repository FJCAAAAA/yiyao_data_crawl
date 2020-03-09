#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetHospitalAndDoctor.py
@Author: Fengjicheng
@Date  : 2020/3/5
@Desc  : 获取医院、医生数据 https://www.guahao.com/
'''
import random
import traceback
import json
from tqdm import tqdm
from main.common.mongo.MongoWriteRead import *
from main.common.WebUtils import *
from main.common.UserAgent import pcUserAgent


class GetHospAndDoc(object):
    def __init__(self):
        self.sec_area = 'txt/sec_area.txt'
        self.fail_url_doc = 'txt/fail_url_doc.txt'
        self.fail_url = 'txt/fail_url_hosp.txt'

    # 医生列表函数
    def get_one_doctor(self, url, first_depart, sec_depart, hosp, level):
        header = {
            'Host': 'www.guahao.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'close',
            'Referer': 'https://www.guahao.com/expert/fastorder'
        }
        soup = get_soup(url, 0, header, 'utf-8')
        message_list = soup.find('div', class_='list')
        if message_list:
            message_soup_list = message_list.find_all('div', class_='g-doctor-item2 g-clear to-margin')
            if message_soup_list:
                for message_soup in message_soup_list:
                    message = message_soup.find('div', class_='g-doc-baseinfo g-left').find('dl')
                    # 医生姓名
                    doctor_name = message.find('dt').a.get_text().strip()
                    # # 职称
                    doctor_title = message.find('dt').get_text().strip().strip(doctor_name).strip()
                    if len(doctor_name) <= 4:
                        # print({'医生姓名': doctor_name, '一级科室':first_depart, '二级科室':sec_depart, '职称': doctor_title, '医院名称': hosp, '医院级别': level})
                        insert('weiyi_doctor', {'医生姓名': doctor_name, '一级科室':first_depart, '二级科室':sec_depart, '职称': doctor_title, '医院名称': hosp, '医院级别': level})
                return True
            else:
                return False
        else:
            return False

    # 获取一家医院医生数据
    def get_one_hosp_doctor(self, url):
        header = {
            'Host': 'www.guahao.com',
            'User-Agent': random.choice(pcUserAgent),
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'close',
            'Referer': 'https://www.guahao.com/expert/fastorder'
        }
        soup = get_soup(url, 0, header, 'utf-8')
        # 医院信息
        hosp_info = soup.find('div', class_='detail word-break')
        hosp_name = hosp_info.h1.strong.get_text().strip()
        lable_name = hosp_info.h3.span.get_text().strip()
        # print(hosp_name, lable_name)
        # 医生科室信息
        depart_soup = soup.find('section', attrs={'id': 'departments'}).find('div', class_='grid-content')
        depart_soup_list = depart_soup.find_all('li', class_='g-clear')
        if depart_soup_list:
            file = open(self.fail_url_doc, 'a', encoding='utf-8')
            for li in depart_soup_list:
                first_depart_name = li.label.get_text().strip()
                # print('############## 一级科室 {} ##############'.format(first_depart_name))
                for span in li.find_all('span'):
                    doctor_url_id = span.a.get('monitor-div-id')
                    if span.a.get('title'):
                        sec_depart_name = span.a.get('title').strip()
                    else:
                        sec_depart_name = span.a.get_text().strip()
                    # print(sec_depart_name, doctor_url_id)
                    # 按照科室查询医生
                    page = 0
                    while True:
                        page += 1
                        doctor_url = 'https://www.guahao.com/department/shiftcase/{}?pageNo={}'.format(doctor_url_id, page)
                        try:
                            result = self.get_one_doctor(url=doctor_url, first_depart=first_depart_name, sec_depart=sec_depart_name,  hosp=hosp_name, level=lable_name)
                        except Exception:
                            print(traceback.format_exc())
                            print('{}爬取失败'.format(','.join([doctor_url, first_depart_name, sec_depart_name, hosp_name, lable_name])))
                            file.write(','.join([doctor_url, first_depart_name, sec_depart_name, hosp_name, lable_name]) + '\n')
                            file.flush()
                        # time.sleep(1)
                        if not result:
                            break
                            # print(sec_depart_url)
            file.close()

    def get_all_doctor(self):
        with open(self.sec_area, 'r', encoding='utf-8') as f:
            area_list = f.readlines()
        for n in tqdm(area_list):
            header = {
                'Host': 'www.guahao.com',
                'User-Agent': random.choice(pcUserAgent),
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Connection': 'close',
                'Referer': 'https://www.guahao.com/expert/fastorder'
            }
            n_dict = json.loads(n)
            first_area = n_dict.get('一级行政区名称')
            first_area_id = n_dict.get('一级行政区ID')
            sec_area = n_dict.get('二级行政区名称')
            sec_area_id = n_dict.get('二级行政区ID')
            page = 0
            while True:
                page += 1
                sec_url = 'https://www.guahao.com/hospital/{}/{}/{}/{}/p{}'.format(first_area_id, first_area, sec_area_id, sec_area, page)
                soup = get_soup(sec_url, 0, header, 'utf-8')
                soup_hosp = soup.find('ul', class_='hos_ul')
                if soup_hosp:
                    for n in soup_hosp.find_all('li', class_='g-hospital-item J_hospitalItem'):
                        hosp_url = n.a.get('href').strip()
                        try:
                            self.get_one_hosp_doctor(hosp_url)
                        except Exception:
                            print("%s 爬取失败" % (hosp_url))
                            with open(self.fail_url, 'a', encoding='utf-8') as f:
                                f.write("%s 爬取失败" % (hosp_url) + '\n')
                            print(traceback.format_exc())
                            continue
                else:
                    break

if __name__ == '__main__':
    obj = GetHospAndDoc()
    # obj.get_one_doctor('https://www.guahao.com/department/shiftcase/125809921947822000?pageNo=7', '心内科', ' 复旦大学附属中山医院', '三级甲等')
    # obj.get_one_hosp_doctor('https://www.guahao.com/hospital/2c71d3f7-e0c2-4279-8ec2-9e9e101b7d37000')
    obj.get_all_doctor()