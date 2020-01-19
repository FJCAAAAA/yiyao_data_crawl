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


def get_page_detail():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split("\t")
        name = line_sp[0]
        url = "http://tag.120ask.com/zhengzhuang" + line_sp[1].strip()

        num = 1
        while not get_page(url, 0):
            if num > 9:
                write_str_to_txt(line + "\n", fail_path)
                print(url, "查询失败")
                break

            print("\n\n\n页面加载失败，5s分钟后重试", url)
            time.sleep(5)

            num = num + 1
        time.sleep(1)


def get_page(url, times):

    soup = get_soup(url, times, header)
    if not soup:
        return 0

    span_list = soup.find_all('span', attrs={'class': 'sp1'})
    name = soup.find('div', attrs={'class': 'place-p'}).text.split('>').pop().strip()
    if span_list:
        dis = list()
        for span in span_list:
            dis.append(span.text.strip())

        dis.remove("疾病名称")
        write_json_to_txt({"症状": name, "可能疾病": "||".join(dis)}, write_detail_path)
        print(name, "写入成功")
    else:
        write_str_to_txt(name+'\t'+url+'\n', fail_path)
        print(name, url, "无可能疾病")
    return 1


if __name__ == '__main__':
    list_page_path = "txt/AskSymList.txt"
    write_detail_path = "txt/ask120/AskSymDetail.txt"
    fail_path = "txt/AskSymFail.txt"

    get_page_detail()
