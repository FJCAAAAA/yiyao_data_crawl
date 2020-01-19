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
import re

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


def get_page_detail():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        name = line_sp[0]
        url = line_sp[1].strip()
        # url = "http://jbk.39.net/gxy/"

        dic_general = try_and_try(url, name, "general")
        dic_symptom = try_and_try(url + "zztz", name, "symptom")
        dic_syndrome = try_and_try(url + "bfbz", name, "syndrome")
        dic_drug = try_and_try(url + "cyyp", name, "drug")

        write_to_txt(str(dict({"疾病名称": name}, **dic_general, **dic_symptom, **dic_syndrome, **dic_drug)).replace("'", "\"") + "\n", write_detail_path)
        print(name, "write success")
        time.sleep(1)


def try_and_try(url, name, type):
    soup = {}
    num = 1
    while not soup:
        if num > 5:
            break

        soup = get_soup(url, name, 0)
        if not soup:
            print("页面加载失败，30s钟后重试", num, url, "\n")
            time.sleep(30)
        else:
            if type == "general":
                soup = parse_general(soup, url, name, 0, 0)
            elif type == "symptom":
                soup = parse_symptom(soup, url, name, 0, 0)
            elif type == "syndrome":
                soup = parse_symptom(soup, url, name, 0, 0)
            elif type == "drug":
                soup = parse_drug(soup, url, name, 0, 0)

            if not soup:
                print("页面加载失败，30s钟后重试", num, url, "\n")
                time.sleep(30)
        num = num + 1
    time.sleep(0.5)
    return soup


def get_soup(url, name, times):
    if times > 9:
        return {}

    try:
        html = requests.get(url=url, headers=header, timeout=(3, 3))
    except urllib3.exceptions.ReadTimeoutError:
        return retry(url, name, times + 1, " timeout try again ")
    except requests.exceptions.ReadTimeout:
        return retry(url, name, times + 1, " timeout try again ")
    except requests.exceptions.ConnectionError:
        return retry(url, name, times + 1, " ConnectionError try again ")

    if str(html) == "<Response [200]>":
        return BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')

    else:
        return retry(url, name, times + 1, " 504 try latter ")


def retry(url, name, times, word):
    print(name, url + word, times)
    time.sleep(0.5)
    return get_soup(url, name, times)


def parse_general(soup, url, name, times, pr_tm):
    ul_list = soup.find_all('ul', attrs={'class': 'information_ul'})
    if ul_list.__len__() == 0:
        if pr_tm > 10:
            return {}

        print("can`t parse", url, pr_tm + 1)
        sp = get_soup(url, name, times)
        return parse_general(sp, url, name, times, pr_tm + 1)
    else:
        dic = {"发病部位": "0",
               "挂号科室": "0",
               "临床检查": "0",
               "多发人群": "0",
               "别名": "0",
               "治疗方法": "0",
               "治愈率": "0",
               "治疗周期": "0"
               }
        for ul in ul_list:
            lis = ul.find_all('li')
            if lis.__len__() == 0:
                print("\n\nno content exist")
                exit(1)

            for li in lis:
                text = li.get_text()
                tac = text.split("：")
                title = tac[0].strip()
                if title in ("在线购药", "是否医保", "传染性", "治疗费用", "常用药品", "典型症状", "并发症"):
                    continue

                desc = "|".join(filter(None, re.split('[，、：\s]', tac[1].strip())))

                dic[title] = desc
        return dic


def parse_symptom(soup, url, name, times, pr_tm):
    article_box = soup.find('div', attrs={'class': 'article_box'})
    pattern = re.compile(r'(^[一-十0-9]+[,.:，、：]{1})|(^[\(（]{1}[一-十0-9]+[\)）]{1})|(^[①-⑨][,.、，：]?)')
    dic_desc = {}
    text_list = article_box.find_all('p', attrs={'class': 'article_text'})
    if text_list:
        for text in text_list:
            tt = text.find('span').get_text()
            ct = "|".join(filter(None, re.split('[,:;，、。：；\s]', text.get_text().replace(tt, ""))))
            dic_desc[tt] = ct

    dic_detail = {}
    art_num = "文章描述"
    art_name = "症状"
    paragraph = article_box.find('div', attrs={'class': 'article_paragraph'})
    if paragraph:
        p_list = paragraph.find_all('p')
        if p_list:
            art_num_n = 0
            art_name_n = 0
            text_list = []
            for p in p_list:
                if p['class'][0] == "article_title_num":
                    if len(text_list):
                        if not art_num_n:
                            dic_detail[art_num] = {}
                        dic_detail[art_num][art_name] = "|".join(text_list)

                    art_num = re.sub(pattern, '', p.get_text())
                    dic_detail[art_num] = {}
                    text_list.clear()
                    art_num_n += 1
                    art_name_n = 0
                elif p['class'][0] == "article_name":
                    if len(text_list):
                        if not art_num_n:
                            dic_detail[art_num] = {}
                        dic_detail[art_num][art_name] = "|".join(text_list)

                    art_name = re.sub(pattern, '', p.get_text())
                    text_list.clear()
                    art_name_n += 1
                else:
                    text_list.append("|".join(filter(None, re.split('[,:;，、。：；\s]', re.sub(pattern, '', p.get_text().strip())))))

            if not art_num_n:
                dic_detail[art_num] = {}
            dic_detail[art_num][art_name] = "|".join(text_list)
    if "zztz" in url:
        return {"症状描述": dic_desc, "症状详情": dic_detail}
    else:
        return {"并发症描述": dic_desc, "并发症详情": dic_detail}


def parse_drug(soup, url, name, times, pr_tm):
    ul_list = soup.find('ul', attrs={'class': 'drug-list'})
    if not ul_list:
        if pr_tm > 10:
            return {}

        print("can`t parse", url, pr_tm + 1)
        sp = get_soup(url, name, times)
        return parse_drug(sp, url, name, times, pr_tm + 1)
    else:
        name_list = ul_list.find_all('a', attrs={'rel': 'nofollow'})
        names = set()
        for name in name_list:
            for nam in filter(None, re.split('[\r\n ]', name.get_text().replace("\n", ""))):
                names.add(nam)

        return {"常用药品": "|".join(names)}


def write_to_txt(content, path):
    try:
        file = open(path, 'a', encoding='utf-8')
        file.write(content)
        file.flush()
    except():
        print('写入失败', content)


if __name__ == '__main__':
    list_page_path = "DisList.txt"
    write_detail_path = "Disease.txt"
    fail_path = "fail.txt"

    get_page_detail()
