#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : GetMD5.py
@Author: Fengjicheng
@Date  : 2020/1/3
@Desc  : 计算MD5
'''
import hashlib

def get_md5(str):
    """
    Gets the MD5 value of the specified string
    :param str:the specified string
    :return:the MD5 value
    """
    fd = hashlib.md5()
    msg = '{}'.format(str)
    fd.update(msg.encode("utf8"))
    return fd.hexdigest()

if __name__ == '__main__':
    str1 = 'appKey=hxkey2019&drugType=01&pageIndex=5&pageSize=10&timestamp=1578023578361hxsecret2019'
    print(get_md5(str1))
