#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetLngLatTengxunBySearch.py
@Author: Fengjicheng
@Date  : 2019/12/30
@Desc  : 通过腾讯地图API获取指定地址经纬度--地点搜索接口，默认取第一个
'''
import requests
import time


class GetLngLatTengxunBySearch(object):
    def __init__(self):
        self.key = 'FRJBZ-UIUWW-LPFRQ-OAX22-GJFD3-WPBRA'

    def geocode_districts(self, district, size, keyword, times):
        if times > 9:
            return 0
        times = times + 1
        url = 'https://apis.map.qq.com/ws/place/v1/search?' \
              'boundary=region(%s,0)&' \
              'page_size=20&' \
              'page_index=%s&' \
              'keyword=%s&' \
              'orderby=_distance&' \
              'key=%s' % (district, size, keyword, self.key)  # size表示返回第几页
        try:
            response = requests.get(url, timeout=10)
        except Exception as e:
            return self.retry(district, size, keyword, times, '%s,try again'%(e))
        content = response.json()
        if content['status'] == 0:
            districts_list = content['data']
            districts_dict = districts_list[0]
            # districts_geo_dict = districts_list[0].get('location')
            # districts_geo_str = '{},{}'.format(districts_geo_dict.get('lat'),districts_geo_dict.get('lng'))
            return districts_dict
        else:
            print('%s 查询失败' % district)

    def retry(self, district, size, keyword, times, word):
        print(district + word, times)
        time.sleep(1)
        return self.geocode_districts(district, size, keyword, times)


if __name__ == '__main__':
    obj = GetLngLatTengxunBySearch()
    geo = obj.geocode_districts('北京', 1, '北京首儿李桥儿童医院', 0)
    print(geo)
