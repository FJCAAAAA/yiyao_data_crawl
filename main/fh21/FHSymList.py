#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
from main.kswys.UserAgent import pcUserAgent
from main.common.WebUtils import *

header = {
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;'
              'q=0.9,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;'
              'v=b3',
    'Accept-Encoding': 'gzip, deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'captchacode=471dPBUbRBdlA8TShJH250wVgxKvuPIk7piJDuaO5lPf8yW%2B0f%2FA;'
              ' saltkey=6882E6%2FL25NDjjb6eYKzHl6saUIrfuMYeS%2BqoKVmtslyju1J;'
              ' bdshare_firstime=1559134535929;'
              ' BAIDU_SSP_lcr=https://www.baidu.com/link?url=gGjpoflz7IXsTOi9jY5A_Auju1Vjxi24a5k2HCbVkgnzyrcQ15YwEiewuBuzr47h&wd=&eqid=eb90ee59001681ec000000025d0997fc;'
              ' UM_distinctid=16b6d79c1374d7-0fa33765357f8f-37c143e-1fa400-16b6d79c138227; '
              'Hm_lvt_5cb24bbadcda645aa43dbd6738c43ccc=1558598892,1558778449,1560909837;'
              ' Hm_lvt_06099b58680385fb6ecf09cf9e30daf3=1559134468,1560915101;'
              ' Hm_lpvt_06099b58680385fb6ecf09cf9e30daf3=1560938741;'
              ' Hm_lpvt_5cb24bbadcda645aa43dbd6738c43ccc=1560938742',
    'Host': 'zzk.fh21.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(pcUserAgent),
    'Referer': 'https://dise.fh21.com.cn/organ/illness/22.html'
}


def get_page_info():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        url_pre = line_sp[0]
        page_num = int(line_sp[1])
        page_now = int(line_sp[2])

        while page_now <= page_num:
            url = "http://zzk.fh21.com.cn/letter/symptoms/" + url_pre + "-" + str(page_now) + ".html"

            num = 1
            while not get_page(url, 0, page_now):
                if num > 5:
                    write_str_to_txt(url, write_fail_path)
                    print(url, "查询失败")
                    break
                print("\n\n\n页面加载失败，5s钟后重试", url)
                time.sleep(5)
                num = num + 1
            page_now = page_now + 1
            time.sleep(1)


def get_page(url, times, page_now):
        soup = get_soup(url, times, header)
        if not soup:
            return 0

        a_list = soup.find('div', attrs={'class': 'border03_body'}).find_all('a')
        if not len(a_list):
            return retry(url, times, " limit try latter ")
        else:
            content = ''
            for a in a_list:
                href = a.get('href')
                if '/symptom/detail/' in href:
                    sym = a.get_text().strip()
                    content += sym + ' ' + href.replace('/symptom/detail/', '') + '\n'

            write_str_to_txt(content, write_list_path)
            print(url, "write success")
            return 1


if __name__ == '__main__':
    list_page_path = "txt/FHSymListPage.txt"
    write_list_path = "txt/FHSymList.txt"
    write_fail_path = "txt/FHSymListFail.txt"

    get_page_info()
