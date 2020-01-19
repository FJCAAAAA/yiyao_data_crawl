#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : DiseaseList9939.py.py
@Author: Fengjicheng
@Date  : 2019/11/19
@Desc  : 爬取疾病、症状的链接
'''

import random
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
import time

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': random.choice(pcUserAgent),
    'Cookie': 'UM_distinctid=16ae421f61a1f5-06a46bc970e867-353166-1fa400-16ae421f61ba18; '
              'CNZZDATA30033562=cnzz_eid%3D1030876382-1558601275-%26ntime%3D1561095027; '
              'Hm_lvt_224d1dc4be80509b8817ce60aca82160=1558605592,1559135410,1561096497; '
              'Hm_lvt_570f165bc826f5c245327416e244a9c5=1558605592,1559135410,1561096497,1561096596; '
              'CNZZDATA30033500=cnzz_eid%3D171731265-1558603315-%26ntime%3D1561098489;'
              ' Hm_lpvt_570f165bc826f5c245327416e244a9c5=1561099398; '
              'Hm_lpvt_224d1dc4be80509b8817ce60aca82160=1561099398',
    'Referer': 'http://jb.9939.com/jbzz/jingbu/',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Host': 'jb.9939.com'
}

def main():
    for i in range(1,1500):

        url = "http://jb.9939.com/jbzz/" + "?page=" + str(i)

        num = 1
        while not get_page(url, 0):
            if num > 5:
                write_str_to_txt(url, write_fail_path)
                print(url, "查询失败")
                break
            print("\n\n\n页面加载失败，5s钟后重试", url)
            time.sleep(5)
            num += 1
        time.sleep(1)


def get_page(url, times):
    soup = get_soup(url, times, header)
    if not soup:
        return 0

    item_list = soup.find_all('div', class_='cation')
    if item_list:
        result = {'疾病': '', '症状': ''}
        for item in item_list:
            flag = item.find('span').text.strip()
            name = item.find('a').text.strip()
            link = item.find('a').get('href').strip().replace('https://jb.9939.com/', '')

            result[flag] += name + '\t' + link + '\n'

        for k, v in result.items():
            if len(v):
                write_str_to_txt(v, write_list_path[k])
                print(url, k, len(v.split('\t'))-1)

        return 1
    else:
        print(url, "未读取到列表")
        return 0


if __name__ == '__main__':
    write_list_path = {'疾病': 'txt/ListDis9939.txt', '症状': 'txt/ListSym9939.txt'}
    write_fail_path = 'txt/ListFail9939.txt'

    main()