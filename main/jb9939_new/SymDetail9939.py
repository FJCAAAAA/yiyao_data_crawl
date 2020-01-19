#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : SymDetail9939.py
@Author: Fengjicheng
@Date  : 2019/11/20
@Desc  : 9939症状详情爬取
'''


import random
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': random.choice(pcUserAgent),
    # 'Cookie': 'UM_distinctid=16ae421f61a1f5-06a46bc970e867-353166-1fa400-16ae421f61ba18; '
    #           'CNZZDATA30033562=cnzz_eid%3D1030876382-1558601275-%26ntime%3D1561095027; '
    #           'Hm_lvt_224d1dc4be80509b8817ce60aca82160=1558605592,1559135410,1561096497; '
    #           'Hm_lvt_570f165bc826f5c245327416e244a9c5=1558605592,1559135410,1561096497,1561096596; '
    #           'CNZZDATA30033500=cnzz_eid%3D171731265-1558603315-%26ntime%3D1561098489;'
    #           ' Hm_lpvt_570f165bc826f5c245327416e244a9c5=1561099398; '
    #           'Hm_lpvt_224d1dc4be80509b8817ce60aca82160=1561099398',
    'Referer': 'http://jb.9939.com/jbzz/jingbu/',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'close',
    'Host': 'jb.9939.com'
}


def main():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    file.close()
    for line in lines:
        line_sp = line.split("\t")
        url = "http://jb.9939.com/" + line_sp[1].strip()

        num = 1
        while not get_page(url, 0):
            if num > 5:
                write_str_to_txt(line + "\n", write_fail_path)
                print(url, "查询失败")
                break

            print("\n\n页面加载失败，5s分钟后重试", url)
            time.sleep(5)

            num = num + 1
        time.sleep(1)


def get_page(url, times):
    jj_soup = get_soup(url+'jianjie', times, header)
    if not jj_soup:
        return 0
    #症状名称
    name = jj_soup.find('div', class_='art_s').text.split('>').pop().strip()
    result = {'症状名称': name, '症状简介': '', '症状起因': '', '预防': '', '检查': '', '可能疾病信息': [], '相关症状': [],
              '宜吃饮食信息': '', '忌吃饮食信息': '', '宜吃饮食种类': '', '宜吃食物': [], '忌吃饮食种类': '', '忌吃食物': [],
              '就诊科室':[]}
    #症状简介
    jj_div = jj_soup.find('div', class_='bshare')
    if jj_div:
        item_for(result, '症状简介', jj_div.find_all('p'), 'str')
    #病症起因
    by_soup = get_soup(url + 'zzqy', times, header)
    if by_soup:
        by_div = by_soup.find('div',class_='spread')
        if by_div:
            item_for(result, '症状起因', by_div.find_all('p'), 'str')
    #预防
    yf_soup = get_soup(url + 'yufang', times, header)
    if yf_soup:
        yf_div = yf_soup.find('div',class_='spread')
        if yf_div:
            item_for(result, '预防', yf_div.find_all('p'), 'str')
    #检查
    jc_soup = get_soup(url + 'jiancha', times, header)
    if jc_soup:
        jc_div = jc_soup.find('div',class_='spread')
        if jc_div:
            item_for(result, '检查', jc_div.find_all('p'), 'str')
        #相关症状
        xgzz_div = jc_soup.find('div',class_='one-block')
        if xgzz_div:
            item_for(result, '相关症状', xgzz_div.find_all('li'), 'list')
        #可能疾病信息
        knjb_ul = jc_soup.find('ul',class_='dissy')
        if knjb_ul:
            knjb_li_list = knjb_ul.find_all('li',class_='with_01')
            bszz_li_list = knjb_ul.find_all('li',class_='with_02')
            jzks_li_list = knjb_ul.find_all('li',class_='with_03')
            knjb = []
            for knjb_li,bszz_li,jzks_li in zip(knjb_li_list,bszz_li_list,jzks_li_list):
                if knjb_li and bszz_li and jzks_li:
                    bszz_ctt = []
                    jzks_ctt = []
                    knjb_ctt = knjb_li.find('a').get('title')
                    for a in bszz_li.find_all('a'):
                        bszz_ctt.append(a.get('title'))
                    for a in jzks_li.find_all('a'):
                        jzks_ctt.append(a.get('title'))
                knjb.append([knjb_ctt,bszz_ctt,jzks_ctt])
            result['可能疾病信息'] = knjb
    #食疗
    page = url.split('/')[-2] + '_shiliao.html'
    with open('9939/%s' % (page), 'r', encoding='utf-8') as f:
        page_ctt = f.read()
    sl_soup = BeautifulSoup(page_ctt, 'html.parser')
    sl_div = sl_soup.find('div', class_='spread')
    sl_list = str(sl_div).split('<b>忌吃饮食</b>')

    for i in sl_list:
        ys_soup = BeautifulSoup(i, 'html.parser')
        zl_soup = ys_soup.find('p')
        sw_soup_list = ys_soup.find_all('p', style=True)

        xx = zl_soup.text
        zl = zl_soup.text
        sw = []

        for sw_soup in sw_soup_list:
            xx += sw_soup.text
            sw.append(re.split('\\s', sw_soup.text)[0].strip())
        if sl_list.index(i) == 0:
            result['宜吃饮食信息'] = xx
            result['宜吃饮食种类'] = zl
            result['宜吃食物'] = sw
        elif sl_list.index(i) == 1:
            result['忌吃饮食信息'] = xx
            result['忌吃饮食种类'] = zl
            result['忌吃食物'] = sw
    #就诊科室
    jzks_div = sl_soup.find('div', class_='third-doc btline mT18')
    item_for(result, '就诊科室', jzks_div.find_all('a'), 'list')

    # 空、"暂无"转换为NAN、文本居首末处理
    result1 = result
    for k,v in result1.items():
        if type(v) == str:
            result[k] = v.strip()
            if v.strip() == "暂无":
                result[k] = 'NAN'
            if v.strip() == "无":
                result[k] = 'NAN'
            if not v.strip():
                result[k] = 'NAN'
        if not v :
            result[k] = 'NAN'

    # 插入数据库
    insert('9939zhengzhuang', result)
    print(name, '成功')

    return 1


if __name__ == '__main__':
    list_page_path = 'txt/ListSym9939.txt'
    write_fail_path = 'txt/ListFail9939.txt'

    main()




