#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : AdaGetToken.py
@Author: Fengjicheng
@Date  : 2019/11/26
@Desc  : 每隔60s查询token，并写入redis
'''

import redis
import time
import requests
import json
import traceback
import datetime


def get_token():
    url = 'https://prod-auth-4.adahealth.net/oauth/token'
    header = {
        'authorization': 'Basic YWRhOjl4Q0dqZFJVcEJaVlVHdzJjVUROcTd2S3JCckFNQUU0',
        'accept': 'application/json;charset=utf-8',
        'user-agent': 'ada-api-js',
        'x-ada-platform': 'android',
        'x-ada-app-version': '2.49.3',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Content-Length': '1410',
        'Host': 'prod-auth-4.adahealth.net',
        # 'Connection': 'Keep-Alive',
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'Cookie': 'route=eb82710af4986dfb3cd014ba19db11ab189995ac'
    }
    data = 'refresh_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI1ZGQ2MjliMjE0YTZlZDAwMDFiODJlMzAiLCJyb2xlcyI6WyJTWU1QVE9NX1RSQUNLRVIiLCJDT05WRVJTQVRJT05fRkVFREJBQ0siLCJCRkZfU1lNUFRPTV9TRUFSQ0giLCJCRkZfQ09ORElUSU9OX1NFQVJDSCJdLCJhdXRob3JpdGllcyI6WyJCRkZfU1lNUFRPTV9TRUFSQ0giLCJTWU1QVE9NX1RSQUNLRVIiLCJDT05WRVJTQVRJT05fRkVFREJBQ0siLCJCRkZfQ09ORElUSU9OX1NFQVJDSCJdLCJjbGllbnRfaWQiOiJhZGEiLCJ1c2Vya2V5IjoiNWRkNjI5YjIxNGE2ZWQwMDAxYjgyZTMwIiwic291cmNlX3BsYXRmb3JtIjpudWxsLCJmZWF0dXJlcyI6WyJTWU1QVE9NX1RSQUNLRVIiLCJDT05WRVJTQVRJT05fRkVFREJBQ0siLCJCRkZfU1lNUFRPTV9TRUFSQ0giLCJCRkZfQ09ORElUSU9OX1NFQVJDSCJdLCJzY29wZSI6WyJhbGwiXSwiYXRpIjoiM2NmOWUwYzYtZjA0Ny00NTk3LWEyYTItMzRjMjY5ZGVlYjllIiwicHJpdmFjeV9zZXR0aW5ncyI6eyJBREFfVVNBR0UiOnRydWUsIkNMSU5JQ0FMX1RSSUFMUyI6dHJ1ZSwiTUlOSU1VTV9MRUdBTF9BR0UiOnRydWUsIlBSSVZBQ1lfUE9MSUNZIjp0cnVlLCJURVJNU19BTkRfQ09ORElUSU9OUyI6dHJ1ZSwiVEhJUkRfUEFSVFlfQ09OU0VOVCI6dHJ1ZX0sImxvY2F0aW9uIjoiQ04iLCJleHAiOjE2MDYxOTI0NDMsImxhbmciOiJlbi1HQiIsImp0aSI6Ijc0MjBkN2M1LTJmZjgtNDI3YS1iM2U5LWZmYzgzN2RkODFhYSJ9.LqhYEyQI642o9mtTmt4QTnVUHjhtKubdFpxd-kspnvBqDbExIggnfA179ziabgUX-08ug35ZtXcZRWkWGYJ688pHGpzX91VramR7dXYBWRozRsww2fnM4ZHdQIoUMzegt3Xv_0WthgxtaE93fJOlTECLksNyRWqcLSuVc7UuIJwmF18gN5bMSyD0q5SS_Cu6CqHpCWX9-ZLfrCMj-AOBF4bCVz5tI9hEqqhd_dX9qPwXomZcwpF1ZhmzM_n2DY1ODn59d5Mn4FVs8TboDhMonVLkcHFUi3-VpmLiO5_EYirztu6K-ldlQ9hbtvQAI--Ak86RiFbNCDUUXflkmcvJ3A&grant_type=refresh_token&language=en-GB'
    response = requests.post(url, data=data, timeout=(5, 5), headers=header)
    access_token = json.loads(response.content.decode('utf-8'))['access_token']
    return access_token

if __name__ == '__main__':
    # 创建连接池
    pool = redis.ConnectionPool(decode_responses=True)
    # 使用连接池对象去链接redis
    r = redis.Redis(connection_pool=pool)
    # 每隔60秒查询一次token并写入redis
    while True:
        try:
            r.set('ada_token', get_token())
            print('%s token查询成功，并写入redis' % (datetime.datetime.now()))
        except Exception:
            print(traceback.format_exc())
        time.sleep(60)
