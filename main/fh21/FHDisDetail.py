#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
from main.common.UserAgent import pcUserAgent
from main.common.WebUtils import *

header = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;'
              'v=b3',
    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'captchacode=471dPBUbRBdlA8TShJH250wVgxKvuPIk7piJDuaO5lPf8yW%2B0f%2FA;'
              'saltkey=6882E6%2FL25NDjjb6eYKzHl6saUIrfuMYeS%2BqoKVmtslyju1J;'
              'Hm_lvt_5cb24bbadcda645aa43dbd6738c43ccc=1558598892,1558778449;'
              'Hm_lvt_06099b58680385fb6ecf09cf9e30daf3=1558601170,1558778449;'
              'Hm_lpvt_06099b58680385fb6ecf09cf9e30daf3=1558928709;'
              'Hm_lpvt_5cb24bbadcda645aa43dbd6738c43ccc=1558928710',
    'Host': 'dise.fh21.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(pcUserAgent),
    'Referer': 'https://dise.fh21.com.cn/organ/illness/22.html'
}

name_map = {
    '发病部位在哪里': '部位',
    '应该挂什么科': '科室',
    '有什么典型症状': '典型症状',
    '应该做哪些检查项目呢': '检查项目',
    '这样的病症传染吗': '传染性',
    '高发人群': '人群'
}


def get_page_detail():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        name = line_sp[0]
        url = line_sp[1].strip()

        num = 1
        while not get_page(url, name, 0):
            if num > 5:
                write_str_to_txt(line + "\n", fail_path)
                print(url, "查询失败")
                break

            print("\n\n\n页面加载失败，5s钟后重试", url)
            time.sleep(5)

            num = num + 1
        time.sleep(1)


def get_page(url, name, times):

    soup = get_soup(url, times, header)
    if not soup:
        return 0

    dl_list = soup.find('div', attrs={'class': 'dise03'}).find_all('dl')
    if dl_list.__len__() == 0:
        return retry(url, name, times, " limit try latter ")
    else:
        dic = {"疾病": name}

        alias = soup.find('ol', attrs={'class': 'dise01'}).find('span')
        if alias:
            alias_f = '||'.join(filter(None, re.split('[()（），、\r\n ]', alias.text.replace('又名', '').strip())))
            if alias_f:
                dic["别名"] = alias_f

        attrs = list(filter(None, re.split('[\s]', soup.find('div', attrs={'id': 'diseTabContainer'}).text)))
        links = soup.find_all('p', attrs={'class': 'dise02b1'})

        for dl in dl_list:
            text = dl.text
            tac = text.split("？")
            title = tac[0].strip()

            if tac[1].strip():  # 判空
                desc = "||".join(filter(None, re.split('[，、\r\n ]', tac[1].strip())))
                dic[name_map[title]] = desc

        i = 0
        for (attr, p) in zip(attrs, links):
            i += 1
            attr_url = 'https://dise.fh21.com.cn' + p.find('a').get('href')
            attr_soup = get_soup(attr_url, 0, header)
            text = re.sub(re.compile(r'\s'), '', attr_soup.find('ul', attrs={'class': 'detailc'}).text)
            dic[attr] = text

        write_json_to_txt(dic, write_detail_path)
        print(name, "写入成功")
        return 1


if __name__ == '__main__':
    list_page_path = "DisList.txt"
    write_detail_path = "DiseaseFH.txt"
    fail_path = "FhDisDetailFail.txt"

    get_page_detail()
