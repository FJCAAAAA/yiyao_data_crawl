#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
from main.common.UserAgent import pcUserAgent
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
              ' UM_distinctid=16b6d79c1374d7-0fa33765357f8f-37c143e-1fa400-16b6d79c138227; Hm_lvt_5cb24bbadcda645aa43dbd6738c43ccc=1558598892,1558778449,1560909837;'
              ' Hm_lvt_06099b58680385fb6ecf09cf9e30daf3=1559134468,1560915101;'
              ' Hm_lpvt_06099b58680385fb6ecf09cf9e30daf3=1560938741;'
              ' Hm_lpvt_5cb24bbadcda645aa43dbd6738c43ccc=1560938742',
    'Host': 'zzk.fh21.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(pcUserAgent),
    'Referer': 'https://dise.fh21.com.cn/organ/illness/22.html'
}


def get_page_detail():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        name = line_sp[0]
        url = line_sp[1].strip()
        # url = "288.html"
        # name = "测试"

        num = 1
        while not get_page("http://zzk.fh21.com.cn/symptom/detail/" + url, name, 0):
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

    box = soup.find('div', attrs={'class': 'z_block08_con'})
    if box:
        dis = list()
        for dt in box.find_all('dt'):
            dis.append(dt.text)
        write_json_to_txt({"症状": name, "可能疾病": "||".join(dis)}, write_detail_path)
        print(name, "写入成功")
    else:
        print(name, "无可能疾病")
    return 1


if __name__ == '__main__':
    list_page_path = "txt/FHSymList.txt"
    write_detail_path = "txt/FHSymDetail.txt"
    fail_path = "txt/SymFail.txt"

    get_page_detail()
