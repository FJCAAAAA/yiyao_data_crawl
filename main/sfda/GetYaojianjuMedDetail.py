#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetYaojianjuMedDetail.py
@Author: Fengjicheng
@Date  : 2020/2/3
@Desc  : 
'''
import threading
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


class GetMedDetail(object):
    def __init__(self, url, file, db_name):
        self.url = url
        self.file = file

    def get_yjj_med_detail(self, url):
        path = 'C:\chromedriver\chromedriver.exe'
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(executable_path=path, chrome_options=option)
        try:
            browser.get(url)
            wait = WebDriverWait(browser, 10)
            tr1_list = browser.find_elements_by_xpath('//table[position()=1]//tr[position()>1]//td[position()=1]')
            tr2_list = browser.find_elements_by_xpath('//table[position()=1]//tr[position()>1]//td[position()=2]')
            med_dict = {}
            if tr1_list and tr2_list:
                for td1 in tr1_list:
                    key = td1.text.strip()
                    value = tr2_list[tr1_list.index(td1)].text.strip()
                    if key:
                        med_dict[key] = value
            insert(db_name, med_dict)
        finally:
            browser.close()
            browser.quit()

    def get_all_yjj_med_detail(self):
        with open(self.file, 'r', encoding='utf-8') as f:
            for num in tqdm(f.readlines()):
                url = 'self.url' + str(num.strip())
                self.get_yjj_med_detail(url)

    def get_all_yjj_med_detail_thread(self):
        threads = []
        with open('txt/yjj_med_id.txt', 'r', encoding='utf-8') as f:
            for i in f.readlines():
                url = 'self.url' + str(i.strip())
                t = threading.Thread(target=self.get_yjj_med_detail, args=(url,))
                threads.append(t)
            num = range(len(threads))
            n = 10
            for x in tqdm([num[i:i + n] for i in range(0, len(num), n)]):
                for y in x:
                    threads[y].start()  # 执行线程的start方法，线程开始执行

                for y in x:
                    threads[y].join()  # 这行线程的join方法，等待线程结束，如果主进程不需要等待线程结束，可以不需要调用join方法。


if __name__ == '__main__':
    # # 国产药品
    # url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=25&tableName=TABLE25&Id='
    # file = 'txt/yjj_med_id.txt'
    # db_name = yaojianju

    # 国家基本药物（2018年版）
    url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=138&tableName=TABLE138&Id='
    file = 'txt/yjj_jb_med_id.txt'
    db_name = 'yaojianju_jb'

    # # 麻醉药品和精神药品品种目录
    # url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=102&tableName=TABLE102&Id='
    # file = 'txt/yjj_mz_med_id.txt'
    # db_name = 'yaojianju_mz
    obj = GetMedDetail(url, file, db_name)
    obj.get_all_yjj_med_detail_thread()

