#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
import main.kswys.UserAgent
from main.common.WebUtils import *
from main.common.UserAgent import pcUserAgent

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
    'User-Agent': random.choice(main.kswys.UserAgent.pcUserAgent),
    'Referer': 'https://dise.fh21.com.cn/organ/illness/22.html'
}


def get_page_info():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        url_pre = line_sp[0]
        # page_num = int(line_sp[1])
        # page_now = int(line_sp[2])
        page_num = 2
        page_now = 2

        while page_now <= page_num:
            url = url_pre + "-" + str(page_now) + ".html"

            num = 1
            while not get_page(url, 0, page_now):
                if num > 5:
                    write_str_to_txt(url, write_fail_path)
                    print(url, "查询失败")
                    break
                print("\n\n页面加载失败，5s分钟后重试", url)
                time.sleep(5)
                num = num + 1
            page_now = page_now + 1
            time.sleep(1)

        break


def get_page(url, times, page_now):
        list_soup = get_soup(url, times, header)

        ul_list_1 = list_soup.find_all('ul', attrs={'class': 'dise_list01'})
        ul_list_2 = list_soup.find_all('ul', attrs={'class': 'dise_list02'})
        if ul_list_1.__len__() == 0:
            return retry(url, times, " limit try latter ")
        else:
            content_str = ""

            if page_now == 1:
                for ul in ul_list_1:
                    for a in ul.find_all('a'):
                        name = a.get_text()
                        link = a.get('href')
                        content_str = content_str + name + " " + link + "\n"
            else:
                if ul_list_2.__len__() > 0:
                    del ul_list_2[0]

            if ul_list_2.__len__() > 0:
                for ul in ul_list_2:
                    for a in ul.find_all('a'):
                        name = a.get_text()
                        link = a.get('href')
                        content_str = content_str + name + " " + link + "\n"

            write_str_to_txt(content_str, write_list_path)
            print(url, "写入成功")
            return 1


if __name__ == '__main__':
    list_page_path = "PageId.txt"
    write_list_path = "DisList.txt"
    write_fail_path = "FHDisListFail.txt"

    get_page_info()
