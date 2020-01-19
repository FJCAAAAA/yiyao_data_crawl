#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : FangJi_Detail.py.py
@Author: Fengjicheng
@Date  : 2019/9/19
@Desc  : 中药方剂爬取 https://db.yaozh.com/fangji/10000002.html
'''
import time
import traceback
from tqdm import tqdm
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

def get_one_page(url):
    header = {
        'Host': 'db.yaozh.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
        'Cookie': 'kztoken=nJail6zJp6iXaJqWl29qaGZvZpSS; his=a%3A10%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpiX%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpuV%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpuY%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpyS%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZJuZ%22%3Bi%3A5%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZZmY%22%3Bi%3A6%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZZqU%22%3Bi%3A7%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZZyU%22%3Bi%3A8%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZpOS%22%3Bi%3A9%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZvZpSS%22%3B%7D; acw_tc=2f624a4f15687071793508181e7af8013e196ee35faf7fb81118c8951abe9d; _ga=GA1.3.1803833789.1568707857; bigdata_use_tips=1; yaozh_mobile=1; kztoken=nJail6zJp6iXaJqWl29qaGZuZpuV; his=a%3A5%3A%7Bi%3A0%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGFsZZaV%22%3Bi%3A1%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZtZ5uS%22%3Bi%3A2%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpeY%22%3Bi%3A3%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpiX%22%3Bi%3A4%3Bs%3A28%3A%22nJail6zJp6iXaJqWl29qaGZuZpuV%22%3B%7D; _ga=GA1.2.1803833789.1568707857; Hm_lvt_65968db3ac154c3089d7f9a4cbb98c94=1568710678%2C1568710717%2C1568710815%2C1568710937; Hm_lpvt_65968db3ac154c3089d7f9a4cbb98c94=1568855541; yaozh_userId=258450; UtzD_f52b_saltkey=CH8h6R55; UtzD_f52b_lastvisit=1568851973; UtzD_f52b_lastact=1568859826%09uc.php%09; yaozh_uidhas=1; yaozh_mylogin=1568855575; acw_tc=2f624a0515687075586824968e0f687caf5859ab921108f4796f3ce3ebd63c; think_language=zh-CN; UtzD_f52b_ulastactivity=1568855572%7C0; UtzD_f52b_creditnotice=0D0D2D0D0D0D0D0D0D4240; UtzD_f52b_creditbase=0D0D0D0D0D0D0D0D0; UtzD_f52b_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; yaozh_logintime=1568859825; yaozh_user=258450%091234; db_w_auth=4240%091234; UtzD_f52b_auth=df69y01hqWqFTeVP1JXx4dCa%2F6cP3Va7gX4ynUilrSlMdQvQh0OUs1nxsYmZIXSBExcDFgN5kSFmLsQTnrTckebF',
        'Upgrade-Insecure-Requests': '1'
    }
    soup = get_soup(url, 0, header)
    table = soup.find('table', class_='table')
    if table:
        tr_list = table.find_all('tr')
        if tr_list:
            detail_dict = {}
            for n in table.find_all('tr'):
                key = n.find('th').get_text().strip()
                value = n.find('span').get_text().strip()
                if key:
                    detail_dict[key] = value
            insert('fangji', detail_dict)
            return 0
            # time.sleep(1)
        else:
            print('内容为空', url)
            return 0
    else:
        print('返回内容异常', url)
        return 1



def get_all_page():
    for num in tqdm(range(34228,34482)): #7776
        url = 'https://db.yaozh.com/fangji/%d.html' %(10000000+num)
        result = get_one_page(url)
        times = 0
        while result:
            print('再次请求',url)
            result = get_one_page(url)
            times = times + 1
            if times > 2:
                print('超过3次，不再尝试')
                break



if __name__ == '__main__':
    try:
        get_all_page()
    except Exception:
        print(traceback.format_exc())