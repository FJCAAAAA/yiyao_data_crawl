#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Get_LngLat.py
@Author: Fengjicheng
@Date  : 2019/9/7
@Desc  :获取经纬度
'''
import requests


# 批量地理编码
def geocode_batch(address_list):
    location_list = []
    num_reqs = len(address_list) // 10 + 1
    for req_index in range(num_reqs):
        sl = slice(req_index * 10, (req_index + 1) * 10)
        address_picked = address_list[sl]  # 用slice提取列表元素
        address = '|'.join(address_picked)  # 用“|”拼接地址
        url = 'https://restapi.amap.com/v3/geocode/geo'
        params = {
            'address':address,
            'key':'',
            'batch':True  # 要传batch参数
        }

        try:
            res = requests.get(url, params, timeout=10)
            for add, geo in zip(address_picked, res.json()['geocodes']):
                if geo['location']:  # 当地址错误时，该地址的location为空
                    # location = map(float, geo['location'].split(','))
                    location = geo['location'].split(',')
                else:
                    print ('address: {} can\'t be geocoded.'.format(add))
                    location = [None] * 2  # 异常值用None代替
                location_list.append(location)
        except Exception as e:
            print(e)
            location_list += [[None, None]] * len(address_picked)

        # 打印进度
        print(req_index + 1, '/', num_reqs, 'done!')

    print('all done!')
    return location_list

# address_list = ['安阳市', '北京市', '保定市', '成都市', '重庆市', '长沙市', '常州市', '长春市', '郴州市', '大连市', '东莞市', '德阳市', '大同市', '佛山市', '福州市', '阜阳市', '广州市', '贵阳市', '赣州市', '桂林市', '杭州市', '合肥市', '哈尔滨市', '黄石市', '惠州市', '邯郸市', '胶州市', '嘉兴市', '济南市', '江阴市', '金华市', '晋中市', '九江市', '景德镇市', '昆明市', '开封市', '廊坊市', '乐山市', '娄底市', '柳州市', '六安市', '马鞍山市', '绵阳市', '茂名市', '眉山市', '南京市', '宁波市', '南昌市', '南宁市', '南通市', '南充市', '宁德市', '彭州市', '莆田市', '萍乡市', '攀枝花市', '青岛市', '泉州市', '清远市', '上海市', '深圳市', '苏州市', '石家庄', '汕头市', '沈阳市', '天津市', '太原市', '武汉市', '无锡市', '温州市', '潍坊市', '芜湖市', '西安市', '厦门市', '湘潭市', '邢台市', '新乡市', '新余市', '襄阳市', '扬州市', '阳江市', '岳阳市', '盐城市', '益阳市', '宜昌市', '郑州市', '珠海市', '镇江市', '株洲市', '自贡市', '中山市', '张家口市', '肇庆市', '湛江市', '漳州市', '遵义市']
# address_list = ['安阳市', '北京市']
# print(geocode_batch(address_list))


