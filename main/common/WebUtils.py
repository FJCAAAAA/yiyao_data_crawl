#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : WebUtils.py.py
@Author: Fengjicheng
@Date  : 2019/1/9
@Desc  : 常用函数
'''

import requests
import time
from bs4 import BeautifulSoup
import urllib3
import re



def get_soup(url, times, header, charset, data=''):
    if times > 9:
        return 0
    times = times + 1
    try:
        if "https://" in url:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            list_html = requests.get(url=url, headers=header, timeout=(20, 20), params=data, verify=False)
        else:
            list_html = requests.get(url=url, headers=header, timeout=(20, 20), params=data)
    except urllib3.exceptions.ReadTimeoutError:
        return retry(url, times, " timeout1 try again ", header, charset, data)
    except requests.exceptions.ReadTimeout:
        return retry(url, times, " timeout2 try again ", header, charset, data)
    except ConnectionResetError:
        return retry(url, times, " ConnectionResetError ", header, charset, data)
    except requests.exceptions.ConnectionError:
        return retry(url, times, " ConnectionError ", header, charset, data)

    # list_html.encoding = 'utf-8'

    if str(list_html) == "<Response [200]>":
        content = str(list_html.content, charset, 'ignore').replace('&#', '').replace('\r','\n')  # bs遇 &# 停止解析，需去除
        # content = str(list_html.content, 'utf-8', 'ignore').replace('&#', '')  # bs遇 &# 停止解析，需去除
        return BeautifulSoup(content, 'html.parser')
        # return BeautifulSoup(content, 'lxml')
    else:
        return retry(url, times, " 504 try latter ", header, charset, data)


def retry(url, times, word, header, charset, data):
    print(url + word, times)
    time.sleep(1)
    return get_soup(url, times, header, charset, data)


def get_picture(url, times, header):
    if times > 9:
        return 0
    times = times + 1
    try:
        if "https://" in url:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            list_html = requests.get(url=url, headers=header, timeout=(20, 20), verify=False)
        else:
            list_html = requests.get(url=url, headers=header, timeout=(20, 20))
    except urllib3.exceptions.ReadTimeoutError:
        return retry1(url, times, " timeout1 try again ", header)
    except requests.exceptions.ReadTimeout:
        return retry1(url, times, " timeout2 try again ", header)
    except ConnectionResetError:
        return retry1(url, times, " ConnectionResetError ", header)
    except requests.exceptions.ConnectionError:
        return retry1(url, times, " ConnectionError ", header)

    if str(list_html) == "<Response [200]>":
        return list_html.content
    else:
        return retry1(url, times, " 504 try latter ", header)


def retry1(url, times, word, header):
    print(url + word, times)
    time.sleep(1)
    return get_picture(url, times, header)


def write_str_to_txt(content, path):
    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


def write_json_to_txt(obj, path):

    content = str(obj).replace("'", "\"") + "\n"

    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


def item_for(dic, title, items, flag):
    if items:
        item_list = list()
        for item in items:
            # item_list.append(item.text.strip())
            item_list.append(item.text)

        if flag == 'list':
            # result = '||'.join(item_list)
            # new_item_list = []
            # for i in item_list:
            #     if i not in new_item_list:
            #         if i.strip():
            #             new_item_list.append(i)
            result = list_uniq(item_list)
        else:
            # result = re.sub(re.compile('\\s'), '', ''.join(item_list))
            # result = ''.join(item_list).strip()
            result = ''.join(item_list)

        dic[title] = result


def list_uniq(item_list):
    if type(item_list) == list:
        new_item_list = []
        for i in item_list:
            if i not in new_item_list:
                i = (i.strip() if type(i) == str else i)
                if i:
                    new_item_list.append(i)
        return new_item_list
    else:
        return item_list


def write_list_to_txt(obj_list, path):

    content = "\n".join(obj_list).replace("'", "\"") + "\n"

    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


def write_bytes(content,path):
    try:
        file = open(path,'wb')
        file.write(content)
        file.flush()
    except():
        print('写入失败',path)
