#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import requests
import random
import time
from bs4 import BeautifulSoup
import yiyao_data_crawl.main.kswys.UserAgent
import urllib3
import re
from lxml import html

header = {
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;'
              'v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'ASP.NET_SessionId=xzlb0t55ulruge55w10mf0je',
    'Host': 'cmkd.hnadl.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(yiyao_data_crawl.main.kswys.UserAgent.pcUserAgent),
    'Referer': 'http://cmkd.hnadl.cn/Search.html?t=Disease'
}


def get_page_detail():
    file_pre = "D://pages/"
    page = 91  # 已有15条
    while page < 225:
        file = open(file_pre + str(page) + '.html', 'r', encoding='utf-8')
        content = file.read()
        file.close()
        get_general(content)

        print("----------------------page", page, "over-----------------------")
        page += 1
        time.sleep(3)


def get_general(content):

    etree = html.etree

    tables = etree.HTML(content).xpath('//*[@id="aspnetForm"]/div/table[3]/tr/td[2]/table/tr[11]/td/table/tr/td[3]/table/tr[2]/td/table')

    for table in tables:
        pattern = re.compile(r'[\s:：]')
        tb_bs = BeautifulSoup(etree.tostring(table), 'html.parser')

        general = {}

        a_list = tb_bs.find_all('a')
        general['name'] = a_list[0].get_text().strip()
        general['pdf_url'] = 'http://cmkd.hnadl.cn' + a_list[1].get('href')

        txtGrey = tb_bs.find_all('td', class_=re.compile('txt'))
        indx = 0
        while indx < len(txtGrey):
            txt = re.sub(pattern, '', txtGrey[indx].get_text())
            if txt in ('英文名', '别名', '所属科目', 'ICD号'):
                general[txt] = txtGrey[indx+1].get_text().strip().replace('；', '|')
                indx += 2
            else:
                indx += 1

        detail = get_detail('http://cmkd.hnadl.cn' + a_list[0].get('href').strip())
        if not len(detail):
            write_to_txt(str(general).replace("'", "\"") + ' http://cmkd.hnadl.cn' + a_list[0].get('href').strip() + "\n", write_fail_path)
            print(general['name'], "query failed")
        else:
            write_to_txt(str(dict(general, **detail)).replace("'", "\"") + "\n", write_detail_path)
            print(general['name'], "succeed")


def get_detail(url):
    bs = get_soup(url, 0)

    pattern_num = re.compile(r'([一二三四五六七八九十0-9]+[,.:，、：]{1})|([\(（]{1}[一二三四五六七八九十0-9]+[\)）]{1})|([①②③④⑤⑥⑦⑧⑨⑩][,.、，：]?)')
    pattern_black = re.compile(r'\s+')
    result = {}
    for content in bs.find_all('td', attrs={'class': 'txtContent'}):
        con_sp = content.get_text().split('：', 1)
        if len(con_sp) < 2:
            continue

        result[con_sp[0].strip()] = re.sub(pattern_black, ' ', re.sub(pattern_num, '', con_sp[1].strip()))

    yp = bs.find('input', value='相关药品')
    if yp:
        yp_url = yp.get('onclick').split("'")[1]
        result['相关药品'] = correlation(yp_url)

    jc = bs.find('input', value='相关检查')
    if jc:
        jc_url = jc.get('onclick').split("'")[1]
        result['相关检查'] = correlation(jc_url)
    return result


def correlation(url):
    bs = get_soup('http://cmkd.hnadl.cn' + url, 0)
    table = bs.find('table', id=re.compile('ctl00_cphCenter'))
    result = []
    if table:
        for a in table.find_all('a'):
            result.append(a.get_text().strip())
    return '|'.join(result)


def get_soup(url, times):
    if times > 9:
        return {}

    time.sleep(1)
    try:
        html = requests.get(url=url, headers=header, timeout=(3, 3))
    except urllib3.exceptions.ReadTimeoutError:
        return retry(url, times + 1, " timeout try again ")
    except requests.exceptions.ReadTimeout:
        return retry(url, times + 1, " timeout try again ")
    except requests.exceptions.ConnectionError:
        return retry(url, times + 1, " ConnectionError try again ")

    if str(html) == "<Response [200]>":
        bs = BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')
        if '用户登陆' in bs.find('title').get_text():
            return retry(url, times + 1, " load ")
        else:
            return bs
    else:
        return retry(url, times + 1, " 504 try latter ")


def retry(url, times, word):
    if word == " load ":
        html = requests.get(url='http://cmkd.hnadl.cn', headers=header, timeout=(3, 3))
        bs = BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')
        print("重新进入首页", bs.find('title').get_text())
    print(url, word, times)
    return get_soup(url, times)


def write_to_txt(content, path):
    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


if __name__ == '__main__':
    write_detail_path = "CmkdDisease.txt"
    write_fail_path = "FailCmkd.txt"

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    get_page_detail()
