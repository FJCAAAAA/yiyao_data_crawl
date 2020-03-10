#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : UploadPicture.py
@Author: Fengjicheng
@Date  : 2019/10/16
@Desc  : 图片上传，将图片名称和链接保存到文件中
'''

import requests
import json
from tqdm import tqdm
from requests_toolbelt.multipart.encoder import MultipartEncoder


def uploadimg(filename):
    #请求地址
    url = 'http://medicine.man.jd.com/upload/image'

    #头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Referer': url,
        'Cookie': 'your cookie'
    }

    multipart_encoder = MultipartEncoder(
        fields = {
          #这里根据服务器需要的参数格式进行修改
            'uploadImg': ('file', open(filename, 'rb'), 'application/octet-stream')
        }
    )
    headers['Content-Type'] = multipart_encoder.content_type
    #请求头必须包含一个特殊的头信息,类似于Content-Type: multipart/form-data; boundary=${bound}
    #注意：这里请求头也可以自己设置Content-Type信息，用于自定义boundary
    r = requests.post(url, data=multipart_encoder, headers=headers)
    data = json.loads(r.text)['data']
    return json.loads(data)['jfsUrl']


if __name__ == '__main__':
    with open('picture_name.txt','r',encoding='utf-8') as f:
        filelist = f.readlines()
    resultfile = 'picture_upload.txt'
    file = open(resultfile,'a',encoding='utf-8')
    for n in tqdm(filelist):
        filename = 'picture/' + n.strip()
        jfsUrl = uploadimg(filename)
        file.write(n.strip() + ' ' + jfsUrl + '\n')
        file.flush()
    file.close()
    # print(uploadimg('20200203.png'))
