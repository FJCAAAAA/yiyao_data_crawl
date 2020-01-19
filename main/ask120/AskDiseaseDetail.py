#!/usr/bin/env python3

# @description 
# @author zhaolonglong9
# @date 2019/5/24

import random
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent

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

item_dic = {
    '概述': 'gaishu',
    '病因': 'bingyin',
    '症状': 'zhengzhuang',
    '检查': 'jiancha',
    '鉴别': 'jianbie',
    '并发症': 'bingfa',
    '预防': 'yufang',
    '治疗': 'zhiliao',
    '饮食': 'yinshi'
}


def get_page_detail():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        line_sp = line.split(" ")
        url = "http://tag.120ask.com/jibing" + line_sp[1].strip()

        num = 1
        while not get_page(url, 0):
            if num > 9:
                write_str_to_txt(line + "\n", fail_path)
                print(url, "查询失败")
                break

            print("\n\n页面加载失败，5s分钟后重试", url)
            time.sleep(5)

            num = num + 1
        time.sleep(1)


def get_page(url, times):

    soup = get_soup(url, times, header)
    if not soup:
        return 0

    div_list = soup.find('div', attrs={'class': 'disease-list-title'})
    name = soup.find('div', attrs={'class': 'place-p'}).text.split('>').pop().strip()
    dic = {"疾病": name}

    if div_list:
        li_list = div_list.find_all('li')
        if li_list:
            item_list = {"挂什么科": "科室", "好发人群": "人群", "治疗周期": "周期", "常用药物": "药物"}

            for li in li_list:
                text_sp = li.get_text().split("：")
                title = text_sp[0].strip()
                desc = text_sp[1].strip()

                if title in item_list.keys():
                    if desc:  # 判空
                        desc = "||".join(filter(None, re.split('[，、\r\n ]|[^0-9]+-', desc)))
                        dic[item_list[title]] = desc

    for k, v in item_dic.items():
        item_soup = get_soup(url+v, 0, header)
        if item_soup:
            div = item_soup.find('div', attrs={'class': 'art_cont'})
            if div:
                dic[k] = re.sub(re.compile('\\s'), '', div.text)

    shi_soup = get_soup(url+"shiliao", 0, header)
    if shi_soup:
        divs = shi_soup.find_all('div', class_=re.compile('dl_'))
        if divs:
            eat = {}
            for div in divs:
                title = div.find('em').text.strip()
                advice = re.sub(re.compile('\\s'), '', div.find('var').text.strip())
                eat[title] = {"建议": advice}

                if div.find('div', class_='swiper-container'):
                    food = "||".join(filter(None, re.split('\\s', div.find('div', class_='swiper-container').text)))
                    eat[title]["食物"] = food
                if div.find('div', class_='bigbox'):
                    reason = re.sub(re.compile('\\s'), '', div.find('div', class_='bigbox').text)
                    eat[title]["理由"] = reason
            dic["食疗"] = eat

    if len(dic) < 2:
        write_str_to_txt(name+" "+url+"\n", fail_path)
        print(name, "解析失败，可能非疾病")
        return 1
    write_json_to_txt(dic, write_detail_path)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), name, "写入成功")
    return 1


if __name__ == '__main__':
    list_page_path = "txt/AskDisListBack.txt"
    write_detail_path = "txt/ask120/AskDisDetail.txt"
    fail_path = "txt/AskDisFail.txt"

    get_page_detail()
