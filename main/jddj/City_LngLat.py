#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : City_LngLat.py.py
@Author: Fengjicheng
@Date  : 2019/9/9
@Desc  :
'''
import re
from yiyao_data_crawl.main.jddj.GoodsDetails_by_ll import get_content
from yiyao_data_crawl.main.common.Get_LngLat import geocode_batch
from yiyao_data_crawl.main.common.Get_districts_ll import *

def get_all_city():
    url_city_all = 'https://daojia.jd.com/client?platCode=H5&appName=paidaojia&channel=&appVersion=7.0.0&jdDevice=&functionId=addresspdj%2FgetCitiesSort&body=%7B%7D'
    result = get_content(url_city_all,'url_city_all')
    city_list = []
    for n in result:
        for m in n['cities']:
            city_list.append(m['areaName'])
    print(len(city_list))
    return city_list
    # geo_city = geocode_batch(city_list)
def get_available_city():
    url_page_home = 'https://daojia.jd.com/client?platCode=h5' \
                    '&appName=paidaojia' \
                    '&channel=' \
                    '&appVersion=7.0.0' \
                    '&jdDevice=' \
                    '&functionId=indexh5%2FgetIndex' \
                    '&body={"coordType":"2","currentPage":"","storeId":"","activityId":"","h5From":"","isglb":"","previewDate":null,"isIndex":false}'
                    # '&lng=%s' \
                    # '&lat=%s' %('%2',longitude,latitude)
    city_list = get_all_city()
    geo_city_list = geocode_batch(city_list)
    pattern = re.compile('医药健康')  # 要找的商品全部再“医药健康”类目下
    available_city_list = []
    for n,m in zip(geo_city_list,city_list):
        url = url_page_home + "&lng=%s" %(n[0]) + "&lat=%s" %(n[1])
        try:
            result = get_content(url,"url_page_home%s"%(m))
        except Exception as e:
            print("%s未开通服务"%(m))
        result_kind = result['data'][1]['data']
        if pattern.findall(str(result)):
            # print(n[0],n[1])
            available_city_list.append(m)
    print(get_available_city)
    return available_city_list
# 返回结果 53
# print(get_available_city())
all_city_list = ['安阳市', '北京市', '保定市', '成都市', '重庆市', '长沙市', '常州市', '长春市', '郴州市', '楚雄州',
                 '池州市', '大连市', '东莞市', '德阳市', '大同市', '佛山市', '福州市', '阜阳市', '广州市', '贵阳市',
                 '赣州市', '桂林市', '杭州市', '合肥市', '哈尔滨市', '黄石市', '惠州市', '邯郸市', '胶州市', '嘉兴市',
                 '济南市', '江阴市', '金华市', '晋中市', '九江市', '景德镇市', '昆明市', '开封市', '廊坊市', '乐山市',
                 '娄底市', '柳州市', '六安市', '马鞍山市', '绵阳市', '茂名市', '眉山市', '南京市', '宁波市', '南昌市',
                 '南宁市', '南通市', '南充市', '宁德市', '彭州市', '莆田市', '萍乡市', '攀枝花市', '青岛市', '泉州市',
                 '清远市', '上海市', '深圳市', '苏州市', '石家庄', '韶关市', '汕头市', '沈阳市', '天津市', '太原市',
                 '武汉市', '无锡市', '温州市', '潍坊市', '芜湖市', '西安市', '厦门市', '湘潭市', '邢台市', '新乡市',
                 '新余市', '襄阳市', '扬州市', '阳江市', '岳阳市', '盐城市', '益阳市', '宜昌市', '郑州市', '珠海市',
                 '镇江市', '株洲市', '自贡市', '中山市', '张家口市', '肇庆市', '湛江市', '漳州市', '遵义市']

available_city_list = ['北京市', '成都市', '重庆市', '长沙市', '常州市', '长春市', '大连市', '东莞市', '佛山市', '福州市',
                       '广州市', '贵阳市', '杭州市', '合肥市', '哈尔滨市', '惠州市', '胶州市', '嘉兴市', '济南市', '江阴市',
                       '昆明市', '廊坊市', '马鞍山市', '绵阳市', '南京市', '宁波市', '南昌市', '南宁市', '南通市', '莆田市',
                       '青岛市', '上海市', '深圳市', '苏州市', '石家庄', '沈阳市', '天津市', '太原市', '武汉市', '无锡市',
                       '温州市', '潍坊市', '芜湖市', '西安市', '厦门市', '湘潭市', '扬州市', '郑州市', '珠海市', '镇江市',
                       '株洲市', '中山市', '湛江市']

print(len(available_city_list))
print(len(all_city_list))
# if __name__ == '__main__':
#     file = open('city_districts.txt','a',encoding='utf-8')
#     for i in available_city_list:
#         file.write(geocode_districts(i,0)+'\n')
#         file.flush()
#     file.close()

# print(get_all_city())
