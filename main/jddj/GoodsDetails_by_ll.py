#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GoodsDetails.py
@Author: Fengjicheng
@Date  : 2019/8/29
@Desc  :京东到家药品详情爬取（按照经纬度）
'''
import requests
import random
import json
import re
import time
from bs4 import BeautifulSoup
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent
from yiyao_data_crawl.main.common.mongo.MongoWriteRead import *


def get_content(url,url_name):
    user_agent = random.choice(pcUserAgent)
    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'close',
        'Host': 'daojia.jd.com',
        'Referer': 'https://daojia.jd.com/html/index.html',
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        response = requests.get(url, headers=header)
        content = response.content.decode('utf-8')
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"请求%s成功" % (url_name))
    except Exception as e:
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),"请求%s失败" %(url_name),e)
    return json.loads(content)['result']

def get_one_goods(goods_skuId,goods_storeId,goods_orgCode):
    url_goods = 'https://daojia.jd.com/client' \
                 '?&platCode=H5' \
                 '&appName=paidaojia' \
                 '&channel=' \
                 '&appVersion=7.0.0' \
                 '&jdDevice=' \
                 '&functionId=product/detailV6_0' \
                 '&body={"skuId":"%s","storeId":"%s","orgCode":"%s","buyNum":1}' %(goods_skuId,goods_storeId,goods_orgCode)
    result = get_content(url_goods,'url_goods')
    goodsname = result['name']
    image = [x['big'] for x in result['image']]
    pattern = re.compile('【|】|\\s')
    pattern2 = re.compile('\\s')
    pattern3 = re.compile('【.*?】')
    detail_dict = {'名称': re.sub(pattern3,'',goodsname), '图片': image}
    if 'detailInfo' in result:
        html = result['detailInfo']['h5HtmlText']
        soup = BeautifulSoup(html,'lxml')
        try:
            for td in soup.find_all('td'):
                detail_list = td.find_all('p')
                if len(detail_list) > 1:
                    detail_key = re.sub(pattern,'',detail_list[0].get_text()).strip()
                    detail_value = re.sub(pattern2, '', detail_list[1].get_text()).strip()
                    detail_title_list = pattern3.findall(detail_value)
                    if detail_title_list:
                        detail_value_content = {}
                        detail_content_list = re.split(pattern3, detail_value)[1:]
                        for n, m in zip(detail_title_list, detail_content_list):
                            detail_value_content[re.sub(pattern, '', n)] = m
                        detail_dict[detail_key] = detail_value_content
                    else:
                        detail_dict[detail_key] = detail_value
        except Exception as e:
            print("%s详情获取异常"%(goodsname),e)
    return detail_dict

def get_one_page(longitude,latitude,activityId):
    url_page = 'https://daojia.jd.com/client' \
               '?platCode=H5' \
               '&appName=paidaojia' \
               '&channel=' \
               '&appVersion=7.0.0' \
               '&jdDevice=' \
               '&functionId=act%sFgetActivityPage' \
               '&body={"longitude":%s,"latitude":%s,"activityId":"%s","shareFlag":null,"coordType":2,"previewDate":null,"ref":"/html/index.html"}' %('%2',longitude,latitude,activityId)
    result = get_content(url_page,'url_page')
    judge = result['data']
    empty_url = 'https://img30.360buyimg.com/mobilecms/jfs/t3256/301/5257118490/24822/c833c937/587eedf8N437d10f7.jpg'
    if re.compile(empty_url).findall(str(judge)):
        print('商品页面为空')
    else:
        goods_type = result['data'][1:] #所有药品列表
        # j2m = JsonToMongo()
        for n in goods_type:
            goods_list = n['data'] #单个选框下的药品列表包括storeId、skuList
            for m in goods_list:
                if 'skuList' in m:
                    skuList = m['skuList'] #药品列表
                    for x in skuList:
                        good_detail = get_one_goods(x['skuId'],x['storeId'],x['orgCode'])
                        # j2m.write_database(good_detail)
                        insert('jddj',good_detail)

def get_activityId():
    url_page_all = 'https://daojia.jd.com/client' \
                   '?platCode=h5' \
                   '&appName=paidaojia' \
                   '&channel=' \
                   '&appVersion=7.0.0' \
                   '&jdDevice=&functionId=channel%2FgetChannelDetail' \
                   '&body={"longitude":116.407394,"latitude":39.904217,"city":"北京市","address":"北京市经济委员会","coordType":"2","channelId":"7","ref":"/html/index.html"}'
    result = get_content(url_page_all, 'url_page_all')
    page_list = result['data'][1]['data'][0]['data']
    with open('activityId.txt','a',encoding='utf-8') as f:
        for n in page_list:
            activityId = n['floorCellData']['params']['activityId']
            page = n['floorCellData']['title']
            f.write(page+' '+activityId+'\n')

def get_all_page(longitude,latitude):
    with open('activityId.txt','r',encoding='utf-8') as f:
        activityId_list = f.readlines()

    for n in activityId_list:
        pa_list = re.split(' ',n.strip())
        activityId = pa_list[1]
        page = pa_list[0]
        try:
            get_one_page(longitude,latitude,activityId)
            print("%s 相关爬取完成" %(page))
        except Exception as e:
            print("%s 相关爬取异常" %(page),e)

if __name__ == "__main__":
    with open('city_districts.txt','r',encoding='utf-8') as f:
        districts_list = f.readlines()
    for n in districts_list:
        districts_dict = json.loads(n.strip())
        for k,v in districts_dict.items():
            get_all_page(v['lng'],v['lat'])
            print('----------------------------------------------%s结束----------------------------------------------'%(k))
            time.sleep(10)