#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Hospital_Detail.py
@Author: Fengjicheng
@Date  : 2019/9/20
@Desc  : 好大夫医院数据爬取 https://www.haodf.com/yiyuan/beijing/list.htm
'''
import random
import json
import traceback
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *
from tqdm import tqdm


class GetHospitalDetail(object):
    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'close',
            'Host': 'www.haodf.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(pcUserAgent)
        }
        self.first_area = 'first_area.txt'
        self.sec_area = 'sec_area.txt'
        self.fail_url = 'fail_url.txt'
        # self.hosp_detail = {}

    # 获取所有一级行政区
    def get_first_area(self):
        url = 'https://www.haodf.com/yiyuan/beijing/list.htm'
        soup = get_soup(url,0,self.header)
        area1 = soup.find('div',class_='kstl2')
        area_list = soup.find_all('div',class_='kstl')
        file = open(self.first_area,'a',encoding='utf-8')
        if area1:
            area = area1.get_text().strip()
            url = 'https:' + area1.a.get('href').strip()
            file.write(area + ' ' + url + '\n')
            file.flush()
        if area_list:
            for n in area_list:
                area = n.get_text().strip()
                url = 'https:' + n.a.get('href').strip()
                file.write(area + ' ' + url + '\n')
                file.flush()
        file.close()
        print("所有省级行政区爬取完成")

    # 获取所有二级行政区
    def get_second_area(self):
        with open(self.first_area,'r',encoding='utf-8') as f:
            area_list = f.readlines()
        for n in area_list:
            n_list = re.split(' ',n)
            first_area = n_list[0]
            first_area_url = n_list[1].strip()
            soup = get_soup(first_area_url,0,self.header)
            ksbd = soup.find('div',class_='ksbd')
            file = open(self.sec_area,'a',encoding='utf-8')
            if ksbd:
                for m in ksbd.find_all('li'):
                    sec_area_url = 'https:' + m.a.get('href').strip()
                    sec_area = m.a.get_text().strip()
                    file.write(first_area + ' ' + sec_area + ' ' + sec_area_url + ' ' + '\n')
                    file.flush()
            else:
                print(first_area,'没有二级行政区')
            file.close()

    # 获取一家医院数据（名称、标签、简介、电话、地址、路线）
    def get_one_hosp(self,url):
        sep1 = re.compile('：')
        hosp_detail = {}
        soup = get_soup(url,0,self.header)
        hdtitle = soup.find('div',class_='h-d-title')
        hosp_name = hdtitle.find('h1',class_='hospital-name').get_text().strip() # 名称
        hosp_detail['名称'] = hosp_name
        lable_list = []
        for n in hdtitle.find_all('span',class_='hospital-label-item'):
            lable_list.append(n.get_text().strip())  # 标签
        hosp_detail['标签'] = lable_list
        hdcontent = soup.find('div',class_='h-d-content')
        hdcitem_list = hdcontent.find_all('p',class_='h-d-c-item')
        intro_link = hdcitem_list[0].find('a',class_='h-d-c-item-link')
        address_link = hdcitem_list[1].find('a',class_='h-d-c-item-link')
        route_link = hdcitem_list[2].find('a',class_='h-d-c-item-link')
        if intro_link:
            intro_url = 'https:' + intro_link.get('href').strip()
            intro_soup = get_soup(intro_url,0,self.header)
            intro = intro_soup.find('td',style='font-size:14px; line-height:20px;').get_text().strip()
        else:
            intro = hdcitem_list[0].find('span',class_='h-d-c-item-text').get_text().strip() # 简介
        hosp_detail['简介'] = intro
        if address_link:
            address_url = 'https:' + address_link.get('href').strip()
            address_soup = get_soup(address_url,0,self.header)
            content = address_soup.find('table',style='margin: 10px 0px 0px 0px')
            for n in content.find_all('tr'):
                td_list = n.find_all('td')
                key = td_list[0].get_text().strip()
                value = td_list[1].get_text().strip()
                hosp_detail[re.sub(sep1,' ',key)] = value
            to_json = json.dumps(hosp_detail,ensure_ascii=False)
            if to_json.find('怎么走'):
                hosp_detail = json.loads(to_json.replace('怎么走', '路线'))
            else:
                hosp_detail['路线'] = hdcitem_list[2].find('span',class_='h-d-c-item-text').get_text().strip()
        elif route_link:
            route_url = 'https:' + route_link.get('href').strip()
            route_soup = get_soup(route_url, 0, self.header)
            content = route_soup.find('table', style='margin: 10px 0px 0px 0px')
            for n in content.find_all('tr'):
                td_list = n.find_all('td')
                key = td_list[0].get_text().strip()
                value = td_list[1].get_text().strip()
                hosp_detail[re.sub(sep1, ' ', key)] = value
            to_json = json.dumps(hosp_detail, ensure_ascii=False)
            if to_json.find('怎么走'):
                hosp_detail = json.loads(to_json.replace('怎么走', '路线'))
            else:
                hosp_detail['路线'] = hdcitem_list[2].find('span', class_='h-d-c-item-text').get_text().strip()
        else:
            hosp_detail['地址'] = hdcitem_list[1].find('span', class_='h-d-c-item-text').get_text().strip()
            hosp_detail['路线'] = hdcitem_list[2].find('span', class_='h-d-c-item-text').get_text().strip()
            hosp_detail['电话'] = hdcontent.find('span', class_='h-d-c-item-text js-phone-text').get_text().strip()
        return hosp_detail

    #获取一家医院数据（名称、排名、特色科室）
    def get_one_hosp1(self, url):
        soup = get_soup(url, 0, self.header)
        hib1 = soup.find('div',class_='hospital-influence-box')
        hib2 = soup.find('div',class_='hp-infl-box')
        hul = soup.find('ul',class_='hospital-o-ul')
        if hib1:
            pass

    def get_all_hosp(self):
        with open(self.sec_area,'r',encoding='utf-8') as f:
            area_list = f.readlines()
        for n in tqdm(area_list):
            n_list = re.split(' ', n)
            first_area = n_list[0]
            sec_area = n_list[1]
            sec_url = n_list[2].strip()
            soup = get_soup(sec_url,0,self.header)
            soup_hosp = soup.find('div',class_='m_ctt_green')
            if soup_hosp:
                for n in soup_hosp.find_all('li'):
                    hosp_url = 'https://www.haodf.com' + n.a.get('href').strip()
                    try:
                        hosp_detail = self.get_one_hosp(hosp_url)
                    except Exception:
                        print("%s 爬取失败" %(hosp_url))
                        with open(self.fail_url,'a',encoding='utf-8') as f:
                            f.write("%s 爬取失败" %(hosp_url) + '\n')
                        print(traceback.format_exc())
                        continue
                    hosp_detail['一级行政区'] = first_area
                    hosp_detail['二级行政区'] = sec_area
                    insert('hospital',hosp_detail)
                    time.sleep(3)
            else:
                print('%s %s 没有医院' %(first_area,sec_area))

    def get_all_hosp1(self):
        with open(self.sec_area,'r',encoding='utf-8') as f:
            area_list = f.readlines()
        for n in tqdm(area_list):
            n_list = re.split(' ', n)
            first_area = n_list[0]
            sec_area = n_list[1]
            sec_url = n_list[2].strip()
            soup = get_soup(sec_url,0,self.header)
            soup_hosp = soup.find('div',class_='m_ctt_green')
            if soup_hosp:
                for n in soup_hosp.find_all('li'):
                    hosp_url = 'https://www.haodf.com' + n.a.get('href').strip()
                    try:
                        hosp_detail = self.get_one_hosp(hosp_url)
                    except Exception:
                        print("%s 爬取失败" %(hosp_url))
                        with open(self.fail_url,'a',encoding='utf-8') as f:
                            f.write("%s 爬取失败" %(hosp_url) + '\n')
                        print(traceback.format_exc())
                        continue
                    insert('hospital_rank',hosp_detail)
                    time.sleep(3)
            else:
                print('%s %s 没有医院' %(first_area,sec_area))

    def get_fail_hosp(self):
        with open(self.fail_url,'r',encoding='utf-8') as f:
            fail_url_list = f.readlines()
        for n in tqdm(fail_url_list):
            fail_url = re.split(' ',n)[0].strip()
            try:
                hosp_detail = self.get_one_hosp(fail_url)
            except Exception:
                print("%s 爬取失败" % (fail_url))
                continue
            insert('hospital', hosp_detail)
            time.sleep(3)




if __name__ == '__main__':
    ghd = GetHospitalDetail()
    # ghd.get_first_area()
    # ghd.get_second_area()
    # ghd.get_all_hosp()
    ghd.get_fail_hosp()