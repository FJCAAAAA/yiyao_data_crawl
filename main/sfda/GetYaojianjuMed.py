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


class GetMedID(object):
    def __init__(self, url, page_num, file, fail_file):
        self.url = url
        self.page_num = page_num
        self.file = file
        self.fail_file = fail_file

    def get_yjj_med_id(self, url):
        file = open(self.file, 'a', encoding='utf-8')
        path = 'C:\chromedriver\chromedriver.exe'
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome(executable_path=path, chrome_options=option)
        # browser = webdriver.Chrome(executable_path=path)

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
            print(browser.page_source)
        finally:
            browser.close()
            browser.quit()
            file.close()
            pass


    def get_all_yjj_med_id(self):
        file =open(self.fail_file, 'a', encoding='utf-8')
        for page in tqdm(range(1, self.page_num)):  #
            try:
                self.get_yjj_med_id(self.url + str(page))
                # print('++++++++++++第 {} 页爬取完成++++++++++++'.format(page))
            except Exception:
                file.write(str(page) + '\n')
                file.flush()
                print('------------第 {} 页爬取失败------------'.format(page))
            # time.sleep(1)
        file.close()

if __name__ == '__main__':
    # # 国产药品
    # url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=25&State=1&bcId=152904713761213296322795806604&tableName=TABLE25&viewtitleName=COLUMN167&viewsubTitleName=COLUMN821,COLUMN170,COLUMN166&curstart='
    # page_num = 11044
    # file = 'txt/yjj_med_id.txt'
    # fail_file = 'txt/fail_yjj_med_id.txt'

    # 国家基本药物（2018年版）
    url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=138&State=1&bcId=152911951192978460689645865168&tableName=TABLE138&viewtitleName=COLUMN1879&viewsubTitleName=COLUMN1876,COLUMN1878,COLUMN1877&curstart='
    page_num = 2  # 47
    file = 'txt/yjj_jb_med_id.txt'
    fail_file = 'txt/fail_yjj_jb_med_id.txt'

    # # 麻醉药品和精神药品品种目录
    # url = 'http://qy1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=102&State=1&bcId=152911939788030557312353847510&tableName=TABLE102&viewtitleName=COLUMN1349&viewsubTitleName=COLUMN1353,COLUMN1350&curstart='
    # page_num = 27
    # file = 'txt/yjj_mz_med_id.txt'
    # fail_file = 'txt/fail_yjj_mz_med_id.txt'

    obj = GetMedID(url, page_num, file, fail_file)
    obj.get_all_yjj_med_id()
