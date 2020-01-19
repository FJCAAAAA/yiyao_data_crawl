#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
from main.common.WebUtils import *
from main.common.UserAgent import pcUserAgent

header = {
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;'
              'v=b3',
    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=169c2f26cf4143-053cbdf56c5cd8-9333061-1fa400-169c2f26cf5989;'
              'comHealthCloudUserProfileUseTag=7ebd7e035bfa8366115c3e767f30ff99;'
              '__jsluid=e675379f573c2468fcf6a69fac2db6e8;'
              'Hm_lvt_7c2c4ab8a1436c0f67383fe9417819b7=1558496173,1558921407,1561011844;'
              'TUSHENGSID=TS1561018240359;'
              'CNZZDATA30036369=cnzz_eid%3D452515503-1558494020-https%253A%252F%252Fwww.120ask.com%252F%26ntime%3D1561026591;'
              'BACKENDASK=jmjqh6u2keiej7p1jlluohu0o1;',
    'Host': 'tag.120ask.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(pcUserAgent),
    'Referer': 'http://tag.120ask.com/zhengzhuang/pinyin/k.html'
}


def get_page_info():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        url = line.strip()

        num = 1
        while get_page(url, 0) == 0:
            if num > 5:
                write_str_to_txt(url, write_fail_path)
                print(url, "查询失败")
                break
            print("\n\n\n页面加载失败，5s钟后重试", url)
            time.sleep(5)
            num = num + 1
        time.sleep(1)


def get_page(url, times):
        soup = get_soup(url, times, header)
        if not soup:
            return 0

        a_list = soup.find('div', attrs={'class': 'internal-medicine'}).find('div').find_all('a')

        if not a_list:
            return retry(url, times, " limit try latter ", header)
        else:
            content_str = ""
            for a in a_list:
                name = a.text
                link = a.get('href')
                content_str += name + "\t" + link + "\n"

            write_str_to_txt(content_str, write_list_path)
            print(url, "写入成功")
            return 1


if __name__ == '__main__':
    list_page_path = "txt/AskSymListPage.txt"
    write_list_path = "txt/AskSymList.txt"
    write_fail_path = "txt/AskSymListFail.txt"

    get_page_info()
