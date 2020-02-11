#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetYaojianjuMed.py
@Author: Fengjicheng
@Date  : 2020/2/3
@Desc  : 爬取药监局药品数据 http://qy1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=25&tableName=TABLE25&title=%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81&bcId=152904713761213296322795806604
'''
import re
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


def get_yjj_med_id(url):
    file = open('txt/yjj_med_id.txt', 'a', encoding='utf-8')
    path = 'C:\chromedriver\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    browser = webdriver.Chrome(executable_path=path, chrome_options=option)

    try:
        browser.get(url)
        wait = WebDriverWait(browser, 10)
        elem_list = browser.find_elements_by_xpath('//table[position()=2]//a')
        if elem_list:
            for elem in elem_list:
                href = elem.get_attribute('href')
                sep1 = re.compile(r"Id=(\d+)'")
                num = sep1.findall(href)
                if num:
                    file.write(num[0] + '\n')
                    file.flush()
    finally:
        browser.close()
        file.close()


def get_all_yjj_med_id():
    file =open('txt/fail_yjj_med_id.txt', 'a', encoding='utf-8')
    for page in tqdm(range(5464, 11053)):  # 5463
        url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&tableName=TABLE25&viewtitleName=COLUMN167&viewsubTitleName=COLUMN821,COLUMN170,COLUMN166&curstart='
        try:
            get_yjj_med_id(url + str(page))
            # print('++++++++++++第 {} 页爬取完成++++++++++++'.format(page))
        except Exception:
            file.write(str(page) + '\n')
            file.flush()
            print('------------第 {} 页爬取失败------------'.format(page))
        # time.sleep(1)
    file.close()

if __name__ == '__main__':
    get_all_yjj_med_id()
