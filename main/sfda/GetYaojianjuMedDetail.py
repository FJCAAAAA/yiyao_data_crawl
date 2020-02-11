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
from main.common.mongo.MongoWriteRead import *


def get_yjj_med_detail(url):
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
        insert('yaojianju', med_dict)
    finally:
        browser.close()
        browser.quit()

def get_all_yjj_med_detail():
    with open('txt/yjj_med_id.txt', 'r', encoding='utf-8') as f:
        for num in tqdm(f.readlines()):
            url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=25&tableName=TABLE25&Id=' + str(num.strip())
            get_yjj_med_detail(url)

def get_all_yjj_med_detail_thread():
    threads = []
    with open('txt/yjj_med_id.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=25&tableName=TABLE25&Id=' + str(i.strip())
            t = threading.Thread(target=get_yjj_med_detail, args=(url,))
            threads.append(t)
        num = range(len(threads))
        n = 10
        for x in tqdm([num[i:i + n] for i in range(0, len(num), n)]):
            for y in x:
                threads[y].start()  # 执行线程的start方法，线程开始执行

            for y in x:
                threads[y].join()  # 这行线程的join方法，等待线程结束，如果主进程不需要等待线程结束，可以不需要调用join方法。


if __name__ == '__main__':
    # get_all_yjj_med_detail()
    get_all_yjj_med_detail_thread()

