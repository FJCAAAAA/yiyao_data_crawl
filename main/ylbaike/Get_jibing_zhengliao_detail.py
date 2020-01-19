#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_jibing_detail.py
@Author: Fengjicheng
@Date  : 2019/8/11
@Desc  :
'''
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import random
import json
import yiyao_data_crawl.main.ylbaike.user_agent
# url = 'https://baike.baidu.com/item/%E7%B3%96%E5%B0%BF%E7%97%85/100969'
agent = random.choice(yiyao_data_crawl.main.ylbaike.user_agent.user_agent_list)
header = {
    'Host': 'baike.baidu.com',
    'User-Agent': agent,
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://baike.baidu.com/wikitag/taglist?tagId=75953',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}
def get_one_page(name,url,file_detail):
    try:
        response = requests.get(url,headers=header)
        html = response.content.decode('utf-8')
    except Exception as e:
        print('该次请求失败，继续下一次请求')
    if BeautifulSoup(html,'lxml').find('div',class_='tashuo-bottom'):
        sep0 = '<div class="tashuo-bottom" id="tashuo_bottom">'
    elif BeautifulSoup(html,'lxml').find('div',class_='lemma-paper-box'):
        sep0 = '<div class="lemma-paper-box">'
    elif BeautifulSoup(html,'lxml').find('div',class_='open-tag-title'):
        sep0 = '<div class="open-tag-title">'
    elif BeautifulSoup(html,'lxml').find('dt',class_='reference-title'):
        sep0 = '<dt class="reference-title">'
    html = re.split(sep0, html)[0]
    soup = BeautifulSoup(html,'lxml')
    summary = soup.find('div',class_='lemma-summary').get_text().strip()
    main_tab = soup.find('div',class_='main_tab main_tab-defaultTab curTab')
    data = {'中文名称': name, '描述': summary}
    if main_tab:
        pass
    else:
        main_tab = soup.find('div', class_='main-content')
    base_info = main_tab.find('div',class_='basic-info cmn-clearfix')
    if  base_info:
        dt_detail = base_info.find_all('dt',class_='basicInfo-item name')
        dd_detail = base_info.find_all('dd',class_='basicInfo-item value')
        for dt,dd in zip(dt_detail,dd_detail):
            data[dt.get_text()]=dd.get_text().strip()
    else:
        print(name,"没有基本信息")
    spe = '<div class="anchor-list">'
    spe2 = '<b>\（[一二三四五六七八九十]{1}\）.*</b>'
    spe3 = '<b>[0-9]{1}.*</b>'
    spe4 = '<b>\（[0-9]{1}\）[^<b>]+</b>'
    content_spe = re.compile(r'([一二三四五六七八九十0-9]+[,.:．，、：]{1})|([\(（]{1}[一二三四五六七八九十0-9]+[\)）]{1})|([①②③④⑤⑥⑦⑧⑨⑩][,.．、，：]?)')
    pattern2 = re.compile(spe2)
    pattern3 = re.compile(spe3)
    pattern4 = re.compile(spe4)
    for i in re.split(spe, html):
        xhtml = etree.HTML(i)
        xtitle = xhtml.xpath('//div[@label-module="para-title"]/h2/text()')
        if xtitle:
            spe1 = '<b>.*</b>'
            pattern1 = re.compile(spe1)
            result11 = pattern1.findall(i)
            if not result11: #没有副标题
                xcontent1 = xhtml.xpath('//*/text()')
                title1 = xtitle[0]
                title1 = re.sub(content_spe,'',title1)
                xcontent_list1 = [x.strip() for x in xcontent1 if x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                content1 = ''.join(xcontent_list1)
                data[title1] = re.sub(content_spe,'',content1)
            else:
                result2 = pattern2.findall(i)
                result3 = pattern3.findall(i)
                result4 = pattern4.findall(i)
                sub_content = {}
                if result2:
                    content_list2 = re.split(spe2, i)[1:]
                    result2_s = pattern2.findall(i)
                    for title2, content2 in zip(result2_s, content_list2):
                        title2_s = BeautifulSoup(title2, 'lxml').get_text()
                        xcontent2_e = etree.HTML(content2)
                        # if result3 and result4: # （一） 1. （1）
                        result2_3 = pattern3.findall(content2)
                        result2_4 = pattern4.findall(content2)

                        if result2_3:
                            content2_list_s = re.split(spe3, content2)
                            sub_sub_content = {}
                            if result2_4:#content2  1. （1）
                                for xtitle_2_3, xcontent2_3 in zip(result2_3, content2_list_s[1:]):
                                    title_2_3 = BeautifulSoup(xtitle_2_3,'lxml').get_text()
                                    result2_4_4 = pattern4.findall(xcontent2_3)
                                    if result2_4_4:
                                        sub_sub_sub_content = {}
                                        xcontent2_4_4_list = re.split(spe4, xcontent2_3)[1:]
                                        for xtitle_2_4_4,xcontent2_4_4 in zip(result2_4_4,xcontent2_4_4_list):
                                            titile_2_4_4 = BeautifulSoup(xtitle_2_4_4,'lxml').get_text()
                                            content2_4_4_e = etree.HTML(xcontent2_4_4)
                                            if content2_4_4_e is not None:
                                                content2_4_4_s = content2_4_4_e.xpath('//*/text()')
                                                content2_4_4_list = [x.strip() for x in content2_4_4_s if x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                                sub_sub_sub_content[re.sub(content_spe, '',titile_2_4_4)] = re.sub(content_spe,'',''.join(content2_4_4_list))
                                            else:
                                                sub_sub_sub_content[re.sub(content_spe, '',titile_2_4_4)] = ''
                                        sub_sub_content[re.sub(content_spe, '',title_2_3)] = sub_sub_sub_content
                                    else:
                                        content2_3_e = etree.HTML(xcontent2_3)
                                        if content2_3_e is not None:
                                            content2_3_s = content2_3_e.xpath('//*/text()')
                                            content2_3_list = [x.strip() for x in content2_3_s if x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                            sub_sub_content[re.sub(content_spe, '', title_2_3)] = re.sub(content_spe,'',''.join(content2_3_list))
                                        else:
                                            sub_sub_content[re.sub(content_spe, '', title_2_3)] = ''
                                sub_content[re.sub(content_spe,'',title2_s)] = sub_sub_content
                            else:# content2 1.
                                for xtitle_2_3, xcontent2_3 in zip(result2_3, content2_list_s[1:]):
                                    title_2_3 = BeautifulSoup(xtitle_2_3,'lxml').get_text()
                                    content2_3_e = etree.HTML(xcontent2_3)
                                    if content2_3_e is not None:
                                        content2_3_s = content2_3_e.xpath('//*/text()')
                                        content2_3_list = [x.strip() for x in content2_3_s if
                                                           x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                        sub_sub_content[re.sub(content_spe, '', title_2_3)] = re.sub(content_spe,'',''.join(content2_3_list))
                                    else:
                                        sub_sub_content[content_spe, '', title_2_3] = ''
                                sub_content[re.sub(content_spe, '', title2_s)] = sub_sub_content

                        else: #content2（一）
                            if  xcontent2_e is not None:
                                content2_s = xcontent2_e.xpath('//*/text()')
                                content2_list = [x.strip() for x in content2_s if
                                                           x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                sub_content[re.sub(content_spe, '', title2_s)] = re.sub(content_spe,'',''.join(content2_list))
                            else:
                                sub_content[re.sub(content_spe, '', title2_s)] = ''
                elif result3:
                    content_list3 = re.split(spe3, i)[1:]
                    if result4: # 1. (1)
                        result3_s = pattern3.findall(i)
                        for title3, content3 in zip(result3_s, content_list3):
                            title3_s = BeautifulSoup(title3, 'lxml').get_text()
                            result4_s = pattern4.findall(content3)  # （1）标题列表
                            if not result4_s:  # 没有类似（1）副标题
                                xcontent3_e = etree.HTML(content3)
                                if xcontent3_e is not None:
                                    xcontent3_s = xcontent3_e.xpath('//*/text()')
                                    content3_1_list = [x.strip() for x in xcontent3_s if
                                                       x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                    sub_content[re.sub(content_spe, '', title3_s)] = re.sub(content_spe,'',''.join(content3_1_list))
                                else:
                                    sub_content[re.sub(content_spe, '', title3_s)] = ''
                            else:
                                sub_sub_content = {}
                                content_list3_1 = re.split(spe4, content3)  # （1）
                                for title3_1_s, content3_1_s in zip(result4_s, content_list3_1[1:]):
                                    title3_1 = BeautifulSoup(title3_1_s, 'lxml').get_text()
                                    xcontent3_1_e = etree.HTML(content3_1_s)
                                    if xcontent3_1_e is not None:
                                        content3_1 = xcontent3_1_e.xpath('//*/text()')
                                        content3_1_list = [x.strip() for x in content3_1 if
                                                           x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                        sub_sub_content[re.sub(content_spe, '', title3_1)] = re.sub(content_spe,'',''.join(content3_1_list))
                                    else:
                                        sub_sub_content[re.sub(content_spe, '', title3_1)] = ''
                                sub_content[re.sub(content_spe, '', title3_s)] = sub_sub_content
                    else:  # 1.
                        for xt3,xc3 in zip(result3,content_list3):
                            title3 = BeautifulSoup(xt3,'lxml').get_text()
                            xcontent3_e = etree.HTML(xc3)
                            if xcontent3_e is not None:
                                xcontent3 = xcontent3_e.xpath('//*/text()')
                                xcontent_list3 = [x.strip() for x in xcontent3 if x.strip() != '' and x.strip() != '，' and x.strip() != '、']
                                sub_content[re.sub(content_spe,'',title3)] = re.sub(content_spe,'',''.join(xcontent_list3))
                            else:
                                sub_content[re.sub(content_spe,'',title3)] = ''
                data[xtitle[0]]= sub_content
    try:
        with open(file_detail,'a',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False)
        print(name,'写入文件成功。')
    except Exception as e:
        print(name,'写入文件失败！')
    # print(data)

def get_all_page():
    with open('jibing_url_uniq.txt', 'r',encoding='utf-8') as f:
        for i in f.readlines():
            a = eval(i.strip('\n'))
            for k, v in a.items():
                try:
                    get_one_page(k,v,'jibing_detail.txt')
                except Exception as e:
                    print(k,v,"爬取失败")
                    print(e)
    with open('zhenliao_url_uniq.txt', 'r',encoding='utf-8') as f:
        for i in f.readlines():
            a = eval(i.strip('\n'))
            for k, v in a.items():
                try:
                    get_one_page(k,v,'zhenliao_detail.txt')
                except Exception as e:
                    print(k,v,"爬取失败")
                    print(e)
    # get_one_page('14C呼气试验','http://baike.baidu.com/item/14C%E5%91%BC%E6%B0%94%E8%AF%95%E9%AA%8C/16305621','test.txt')
if __name__ == "__main__":
    try:
        get_all_page()
    except Exception as e:
        print(e)