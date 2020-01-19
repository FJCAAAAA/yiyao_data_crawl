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
        'Cookie': '__jda=101385626.1565925994758990536265.1565925995.1577965693.1578013804.352; __jdu=1565925994758990536265; TrackID=1cZMwY5-dym4BkoDbSd8s-qZ-YkTtgtPgOwd_BuXjrhfRF5eedKcrljas1GuCQRxvsKmjXmIM-EPk7Va-JAcN_3MtCrcyDOCS6SdMWLQfpA-U4PHvxga3VewjWQeycC9o; pinId=tBQUB3AYXIRR5Wpdorwm3A; shshshfp=6e62d1d83949534bb18f96480e1f913e; shshshfpa=211ad900-bac7-8b61-42b3-c82cc7f72fdc-1566537958; shshshfpb=toORyKTnnp3cHkzs0C1fhyw%3D%3D; _tp=tdP1A4BCTzqzLITkNH6tQ0HKmE5Ackgis70h6sb9P5QiK5mirKCyNrcfC5kq629E; _pst=%E6%83%A0%E5%B7%9E%E5%A4%A7%E8%8D%AF%E6%88%BF; ipLoc-djd=1-2809-51216-0; jd.erp.lang=zh_CN; mba_muid=1565925994758990536265; TrackerID=So-BLe5wrSwwBxb3lewQCGCK99uboPOBxfbsYfva0sbtygIyrzgfZu2rq03PWRDSQaUhJ3rruoRXvCxjlLPcSzAXw36ljbg-sO2QbUfZjyA3pBlc78007HagQ1-34D00; 3AB9D23F7A4B3C9B=PF4UR2DKDPP27JNFFRPGHJ4RFC766TFLJNWB4DUACOE2ESAJOBQ4SGWSQEY7ISGBLY54MRJY4IDYO4HMPXVQQQG67Q; __jdv=132659215|direct|-|none|-|1577668118992; erp1.jd.com=AFBFAFB1FD9EF5E3492B4DD56D686FFA27856879E389E384D1488E620215405991EF9E7C2F78B05C21F121CCEE9B622A0734099C776051076F36D69578B2B23B2049D20A4E187519CFD69F77D9A7994B; sso.jd.com=BJ.0c705460a96f44df96f1549192ef3738; __jdc=101385626; thor=2217328FB90C3718EF0A3FB612CFA59761EC17C715FD1B33FA087E8A554B76536A23F6757FA241FB5056A44F55374AABDED08606F3A5DC18A11360CCB8047B0EE7EBDDA9309B28A7C353418FCF067BA3A9E851AE722E026BB295726E516CD39C7D943B983E4BA21619C7C702CAF1AF13FE81005E3E1FC27FC53F4CCEFAAF868D; pin=%E6%83%A0%E5%B7%9E%E5%A4%A7%E8%8D%AF%E6%88%BF; unick=%E6%83%A0%E5%B7%9E%E5%A4%A7%E8%8D%AF%E6%88%BF; ceshi3.com=000; logining=1'
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