#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : UploadPicture.py
@Author: Fengjicheng
@Date  : 2019/10/16
@Desc  : 图片上传，将图片名称和链接保存到文件中
'''
import os
import traceback
import requests
import json
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder
from selenium import webdriver


def get_cookie():
    url = 'http://ssa.jd.com/sso/login?ReturnUrl=http%3A%2F%2Fmedicine.man.jd.com%2F'
    username = ''
    password = ''
    browser = webdriver.Chrome()
    try:
        browser.get(url)
        browser.implicitly_wait(3)
        user_input = browser.find_element_by_id('username')
        user_input.send_keys(username)
        pass_input = browser.find_element_by_id('password')
        pass_input.send_keys(password)
        button = browser.find_element_by_class_name('formsubmit_btn')
        button.click()
        global my_cookies
        cookies = browser.get_cookies()
        my_cookies = '; '.join(['='.join([x.get('name'), x.get('value')]) for x in cookies])
    finally:
        browser.close()


def uploadimg(filename):
    url = 'http://medicine.man.jd.com/upload/image'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Referer': url,
        'Cookie': my_cookies
    }
    multipart_encoder = MultipartEncoder(
        fields={
            # 这里根据服务器需要的参数格式进行修改
            'uploadImg': ('file', open(filename, 'rb'), 'application/octet-stream')
        }
    )
    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息,类似于Content-Type: multipart/form-data; boundary=${bound}
    # 注意：这里请求头也可以自己设置Content-Type信息，用于自定义boundary
    r = requests.post(url, data=multipart_encoder, headers=headers)
    # time.sleep(0.5)
    data = json.loads(r.text)['data']
    return json.loads(data).get('jfsUrl')
    # return r.text


def from_file(read_file, write_file, picture_dir=''):
    '''
    从文件读取需要上传的图片名称
    :param read_file: 
    :param write_file: 
    :param picture_dir: 图片路径，默认为空
    :return: 
    '''
    with open(read_file, 'r', encoding='utf-8') as f:
        filelist = f.readlines()
    file = open(write_file, 'a', encoding='utf-8')
    for n in tqdm(filelist):
        filename = picture_dir + n.strip()
        try:
            jfsUrl = uploadimg(filename)
            file.write(n.strip() + ' ' + jfsUrl + '\n')
            file.flush()
        except Exception:
            print(traceback.format_exc())
            continue
    file.close()



def list_dir(picture_dir):
    '''
    列出指定目录文件
    :param picture_dir: 
    :return: 
    '''
    files = []
    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(picture_dir)
    for i in range(0, len(list_file)):
        # 构造路径
        path = os.path.join(picture_dir, list_file[i])
        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归
        if os.path.isdir(path):
            files.extend(list_dir(path))
        if os.path.isfile(path):
            files.append(path)
    return files


def from_dir(picture_dir, write_file):
    '''
    从目录查找要上传的图片
    :param picture_dir: 
    :param write_file: 
    :return: 
    '''
    files = list_dir(picture_dir)
    file_ = open(write_file, 'a', encoding='utf-8')
    for n in tqdm(files):
        try:
            jfsUrl = uploadimg(n)
            file_.write(n.strip().split('/')[-1] + ' ' + jfsUrl + '\n')
            file_.flush()
        except Exception:
            print(traceback.format_exc())
            continue
    file_.close()


if __name__ == '__main__':
    # print(list_dir('E:/爬虫项目/饿了么/picture/'))
    # print(len(list_dir('E:/爬虫项目/饿了么/picture/')))
    # from_dir('E:/爬虫项目/饿了么/picture/', 'D:/project/yiyao_data_crawl/yiyao_data_crawl/main/elem/DataProcessing/upload_file.txt')
    # file = open('D:/project/yiyao_data_crawl/yiyao_data_crawl/main/elem/DataProcessing/picture.txt', 'a', encoding='utf-8')
    # for i in list_dir('E:/爬虫项目/饿了么/picture/'):
    #     file.write(i + '\n')
    #     file.flush()
    # file.close()

    # from_file('D:/project/yiyao_data_crawl/yiyao_data_crawl/main/elem/DataProcessing/picture.txt',
    #           'D:/project/yiyao_data_crawl/yiyao_data_crawl/main/elem/DataProcessing/upload_file.txt')

    get_cookie()
    print(uploadimg('E:\爬虫项目\京药通\picture\8aef82b26cfb54d1016cfb63a6b501a2_0.jpg'))

