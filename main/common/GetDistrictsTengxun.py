#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_districts_ll.py.py
@Author: Fengjicheng
@Date  : 2019/9/9
@Desc  : 通过腾讯地图API搜索不同城市"指定地点"及"坐标"
'''
import requests
import time
import json
from tqdm import tqdm


class SearchDistricts(object):
    def __init__(self):
        self.keyword = '小区'
        self.key = ''

    def geocode_districts(self, district, size, times):
        if times > 9:
            return 0
        times = times + 1
        url = 'https://apis.map.qq.com/ws/place/v1/search?' \
              'boundary=region(%s,0)&' \
              'page_size=20&' \
              'page_index=%s&' \
              'keyword=%s&' \
              'orderby=_distance&' \
              'key=%s' % (district, size, self.keyword, self.key)  # size表示返回第几页
        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            return self.retry(district, size, times, '%s,try again'%(e))
        content = response.json()
        if content['status'] == 0:
            districts_dict = {}
            districts_list = content['data']
            for n in districts_list:
                districts_dict[n['title']] = n['location']
            # print('%s 第%s叶查询成功' % (district, size))
            return json.dumps({district: districts_dict}, ensure_ascii=False)
        else:
            print('%s 查询失败' % district)

    def retry(self, district, size, times, word):
        print(district + word, times)
        time.sleep(1)
        return self.geocode_districts(district, size, times)

    def get_all(self, city_list, filename):
        file = open(filename, 'a', encoding='utf-8')
        for city in tqdm(city_list):
            file.write(self.geocode_districts(city, 1, 0) + '\n')
            file.flush()
            time.sleep(1)  # 并发限制每秒5次，所以这里设置睡眠时间
        file.close()

if __name__ == '__main__':
    available_city_list = ['北京市', '成都市', '重庆市', '长沙市', '常州市', '长春市', '大连市', '东莞市', '佛山市', '福州市',
                           '广州市', '贵阳市', '杭州市', '合肥市', '哈尔滨市', '惠州市', '胶州市', '嘉兴市', '济南市', '江阴市',
                           '昆明市', '廊坊市', '马鞍山市', '绵阳市', '南京市', '宁波市', '南昌市', '南宁市', '南通市', '莆田市',
                           '青岛市', '上海市', '深圳市', '苏州市', '石家庄', '沈阳市', '天津市', '太原市', '武汉市', '无锡市',
                           '温州市', '潍坊市', '芜湖市', '西安市', '厦门市', '湘潭市', '扬州市', '郑州市', '珠海市', '镇江市',
                           '株洲市', '中山市', '湛江市']
    available_city_list1 = ['北京市']
    obj = SearchDistricts()
    obj.get_all(available_city_list1, 'city_districts.txt')
