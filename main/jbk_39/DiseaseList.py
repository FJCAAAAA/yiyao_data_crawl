#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import requests
import random
import time
from bs4 import BeautifulSoup
import main.kswys.UserAgent
import urllib3

header = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;'
              'v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'Cookie: disv_925181=%E6%B0%94%E7%AE%A1%E7%82%8E%7Chttp%3A%2F%2Fjbk.39.net%2Fqgy1%2F%7C1558599519989;'
              ' Hm_lvt_eefa4d8db0fa9214fbd06e08764b6cdc=1558599520;'
              ' Hm_lvt_0711a4f91bc0a9d22a67012693562b07=1558599520;'
              ' disv_326321=%E9%9D%92%E5%85%89%E7%9C%BC%7Chttp%3A%2F%2Fjbk.39.net%2Fqgy%2F%7C1558606803307;'
              ' disv_298734=%E7%99%BE%E6%97%A5%E5%92%B3%7Chttp%3A%2F%2Fjbk.39.net%2Fbrk%2F%7C1558606826171;'
              ' disv_347702=%E9%93%8B%E4%B8%AD%E6%AF%92%7Chttp%3A%2F%2Fjbk.39.net%2Fbzd%2F%7C1558606972446;'
              ' disv_347739=%E8%8B%AF%E4%B8%AD%E6%AF%92%7Chttp%3A%2F%2Fjbk.39.net%2Fbzd1%2F%7C1558607242383;'
              ' disv_298730=%E6%84%9F%E5%86%92%7Chttp%3A%2F%2Fjbk.39.net%2Fgm%2F%7C1558663969811;'
              ' Hm_lvt_ab2e5965345c61109c5e97c34de8026a=1558666955;'
              ' Hm_lpvt_ab2e5965345c61109c5e97c34de8026a=1558666955;'
              ' disv_318607=%E5%8F%A3%E8%85%94%E6%BA%83%E7%96%A1%7Chttp%3A%2F%2Fjbk.39.net%2Fkqky%2F%7C1558667485912;'
              ' disv_643433=%E8%83%83%E6%BA%83%E7%96%A1%7Chttp%3A%2F%2Fjbk.39.net%2Fwky%2F%7C1558668948156;'
              ' Hm_lpvt_eefa4d8db0fa9214fbd06e08764b6cdc=1558684409;'
              ' Hm_lpvt_0711a4f91bc0a9d22a67012693562b07=1558684409',
    'Host': 'jbk.39.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(main.kswys.UserAgent.pcUserAgent),
    'Referer': 'http://jbk.39.net/bw/t1/'
}


def get_page_info():
    url_pre = "http://jbk.39.net/bw/"

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        url_mid = line_sp[0]
        page_num = int(line_sp[1])
        page_now = int(line_sp[2])

        while page_now <= page_num:
            url = url_pre + url_mid + "_p" + str(page_now)

            num = 1
            while get_page(url, 0) == 0:
                if num % 5 == 0:
                    print("\n\n\n页面加载失败，16分钟后重试", url)
                    time.sleep(1000)
                else:
                    print("\n\n\n页面加载失败，5分钟后重试", url)
                    time.sleep(300)
            page_now = page_now + 1
            time.sleep(0.5)


def get_page(url, times):
    if times > 10:
        return 0

    times = times + 1
    try:
        list_html = requests.get(url=url, headers=header, timeout=(3, 3))
    except urllib3.exceptions.ReadTimeoutError:
        return retry(url, times, " timeout try again ")
    except requests.exceptions.ReadTimeout:
        return retry(url, times, " timeout try again ")
    except requests.exceptions.ConnectionError:
        return retry(url, times, " ConnectionError try again ")

    if str(list_html) == "<Response [200]>":
        list_soup = BeautifulSoup(list_html.content, 'html.parser', from_encoding='utf-8')

        item_list = list_soup.find_all('p', attrs={'class': 'result_item_top_l'})
        if item_list.__len__() == 0:
            return retry(url, times, " limit try latter ")
        else:
            content_str = ""
            for item in item_list:
                a = item.find('a')

                b = a.get('title')
                c = a.get('href')
                content_str = content_str + b + " " + c + "\n"

            write_to_txt(content_str, write_list_path)
            print(url, "写入成功")
            return 1

    else:
        return retry(url, times, " 504 try latter ")


def retry(url, times, word):
    print(url + word, times)
    time.sleep(2)
    return get_page(url, times)


def write_to_txt(content, path):
    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


if __name__ == '__main__':
    # 疾病读写路径
    list_page_path = "DisPartList.txt"
    write_list_path = "DisList.txt"
    # 症状读写路径
    # list_page_path = "SymPartList.txt"
    # write_list_path = "SymList.txt"

    get_page_info()
