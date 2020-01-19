#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : DisDetail9939.py
@Author: Fengjicheng
@Date  : 2019/11/19
@Desc  : 9939疾病详情爬取
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
    'Referer': 'https://jb.9939.com/jbzz/jingbu/',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'close',
    'Host': 'jb.9939.com'
}

item_dic = {'发病部位': '发病部位', '别名': '疾病别名', '多发人群': '多发人群'}
pattern1 = re.compile(r'[,.．、，：。？]?')


def main():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    file.close()
    for line in lines:
        line_sp = line.split("\t")
        url = "https://jb.9939.com/" + line_sp[1].strip()

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
    # 疾病名称
    name = jj_soup.find('div', class_='art_s').text.split('>').pop().strip()
    result = {'疾病名称': name, '疾病简介': '', '疾病别名': [], '发病部位': [], '传染性': '', '传播途径': '', '多发人群': '',
              '典型症状': [], '相关疾病': [], '就诊科室': [], '常用药品': [], '相关症状': [], '症状内容': '', '发病原因': '',
              '预防措施': '', '检查项目': [], '检查内容': '', '鉴别': '', '治疗方式': [], '治疗内容': '', '护理': '', '并发症': [],
              '并发症内容': ''}
    #疾病简介
    gai_div = jj_soup.find('div', class_='bshare')
    if gai_div:
        item_for(result, '疾病简介', gai_div.find_all('p'), 'str')
    #是否医保、疾病别名、发病部位、传染性、传播途径、多发人群
    jj_items_div = jj_soup.find('div', class_='protex')
    if jj_items_div:
        for p in jj_items_div.find_all('p'):
            title = p.text.split('：')[0].strip()
            a_list = p.find_all('a',title=True)
            if a_list:
                ctt = list_uniq([a.get('title') for a in a_list])
            else:
                ctt = p.text.split('：')[1].strip()
            # title = p.text.split('：')[0].strip()
            # ctt1 = p.text.split('：')[1].strip()
            # if ctt1 == '暂无':
            #     ctt2 = 'NAN'
            # else:
            #     ctt2 = list(filter(None, re.split('[\\s]', ctt1)))
            # ctt = (ctt2 if title in ['别名','发病部位'] else ctt1)
            #更换字段名称
            if title in item_dic:
                result[item_dic[title]] = ctt
            else:
                result[title] = ctt
        #相关疾病
        xgjb_items_div = jj_items_div.find_all('div',class_='stat disn')
        if xgjb_items_div:
            xgjb = []
            for a in xgjb_items_div[1].find_all('a'):
                xgjb.append(a.get('title'))
            result['相关疾病'] = xgjb
    #就诊科室
    ke_div = jj_soup.find('div', class_='aknol')
    if ke_div:
        ke_a = ke_div.find('p').find_all('a')
        if ke_a:
            item_for(result, '就诊科室', ke_a, 'list')
        else:
            result['就诊科室'] = ke_div.find('p').get_text().split('：')[1].strip()
    #常用药品
    med_div = jj_soup.find('div', class_='refl')
    if med_div:
        item_for(result, '常用药品', med_div.find_all('a'), 'list')
    #相关症状
    xgzz_div = jj_soup.find('div',class_='one-block')
    if xgzz_div:
        item_for(result, '相关症状', xgzz_div.find_all('li'), 'list')
    #典型症状、症状内容
    zz_soup = get_soup(url+'zz', times, header)
    if zz_soup:
        zz_div = zz_soup.find('div', class_='spread')
        if zz_div:
            item_for(result, '典型症状', zz_div.find_all('a', title=True), 'list')
            item_for(result, '症状内容', zz_div.find_all('p', style=True), 'str')
            if result.get('症状内容'):
                result['症状内容'] = zz_div.find('p', class_='spea').get_text() + result.get('症状内容')
            else:
                result['症状内容'] = zz_div.find('p', class_='spea').get_text()
    #发病原因
    by_soup = get_soup(url+'by', times, header)
    if by_soup:
        by_div = by_soup.find('div',class_='spread')
        if by_div:
            item_for(result, '发病原因', by_div.find_all('p', style=True), 'str')
            if result.get('发病原因'):
                result['发病原因'] = by_div.find('p', class_='spea').get_text() + result.get('发病原因')
            else:
                result['发病原因'] = by_div.find('p', class_='spea').get_text()
    #预防措施
    yf_soup = get_soup(url+'yf', times, header)
    if yf_soup:
        yf_div = yf_soup.find('div', class_='spread')
        if yf_div:
            item_for(result, '预防措施', yf_div.find_all('p', style=True), 'str')
            if result.get('预防措施'):
                result['预防措施'] = yf_div.find('p', class_='spea').get_text() + result.get('预防措施')
            else:
                result['预防措施'] = yf_div.find('p', class_='spea').get_text()
    #检查项目、检查内容
    jc_soup = get_soup(url+'lcjc', times, header)
    if jc_soup:
        jc_div = jc_soup.find('div', class_='spread')
        if jc_div:
            item_for(result, '检查项目', jc_div.find_all('a', style=True), 'list')
            item_for(result, '检查内容', jc_div.find_all('p', style=True), 'str')
            if result.get('检查内容'):
                result['检查内容'] = jc_div.find('p',class_='spea').get_text() + result.get('检查内容')
            else:
                result['检查内容'] = jc_div.find('p', class_='spea').get_text()
    #鉴别
    jb_soup = get_soup(url+'jb', times, header)
    if jb_soup:
        jb_div = jb_soup.find('div', class_='spread')
        if jb_div:
            item_for(result, '鉴别', jb_div.find_all('p', style=True), 'str')
            if result.get('鉴别'):
                result['鉴别'] = jb_div.find('p',class_='spea').get_text() + result.get('鉴别')
            else:
                result['鉴别'] = jb_div.find('p', class_='spea').get_text()
    #治疗方式、治疗内容
    zl_soup = get_soup(url+'zl', times, header)
    if zl_soup:
        zl_div = zl_soup.find('div', class_='spread')
        if zl_div:
            zlfs = zl_div.find('p')
            if zlfs:
                result['治疗方式'] = list(filter(None, re.split('[\\s,，、]', zlfs.text)))
            item_for(result, '治疗内容', zl_div.find_all('p', style=True), 'str')
            if result.get('治疗内容'):
                result['治疗内容'] = zl_div.find('p', class_='spea').get_text() + result.get('治疗内容')
            else:
                result['治疗内容'] = zl_div.find('p', class_='spea').get_text()
    #护理
    hl_soup = get_soup(url+'yshl', times, header)
    if hl_soup:
        hl_div = hl_soup.find('div', class_='spread')
        if hl_div:
            item_for(result, '护理', hl_div.find_all('p', style=True), 'str')
            if result.get('护理'):
                result['护理'] = hl_div.find('p',class_='spea').get_text() + result.get('护理')
            else:
                result['护理'] = hl_div.find('p', class_='spea').get_text()
    #并发症内容、并发症
    bfz_soup = get_soup(url+'bfz', times, header)
    if bfz_soup:
        bfz_div = bfz_soup.find('div', class_='spread')
        if bfz_div:
            item_for(result, '并发症内容', bfz_div.find_all('p', style=True), 'str')
            if result.get('并发症内容'):
                result['并发症内容'] = bfz_div.find('p', class_='spea').get_text() + result.get('并发症内容')
                bfz_list = []
                for bfz in filter(None,re.split('[\\s]', result.get('并发症内容'))):
                    if re.match('^\d\..*?', bfz):
                        bfz_cct = re.split('\d\.', bfz)[1].strip()
                        if '其他' not in bfz_cct:
                            bfz_list.append(re.sub(pattern1,'',bfz_cct))
                result['并发症'] = bfz_list
            else:
                result['并发症内容'] = bfz_div.find('p', class_='spea').get_text()


    # write_json_to_txt(result, write_dis_path)
    #空、"暂无"转换为NAN
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


    #删除不需要字段
    result.pop('是否属于医保')
    #插入数据库
    insert('9939jibing',result)
    print(name, '成功')
    return 1


if __name__ == '__main__':
    list_page_path = 'txt/ListDis9939.txt'
    write_fail_path = 'txt/ListFail9939.txt'

    main()