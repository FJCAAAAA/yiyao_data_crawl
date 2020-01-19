#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : picture_upload.py
@Author: Fengjicheng
@Date  : 2019/10/16
@Desc  :
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
        'Cookie':'__jda=50436146.1565925994758990536265.1565925995.1571203959.1571207329.166; __jdu=1565925994758990536265; TrackID=16oHV_UsnMI7kO3DEPG01nEXt3A00y9WDuKD-zqv8h1EEg0eCdWnl7ceQo9kLZiqLjgJJLPKD5ocUcdWQUeweWAlXcLHL0O_k86-ZcWR2BGQBwn-RLMDwZKi0cHsXxEbB; pinId=lEOWdda3K23JVV-5x9T2I3JkvqlpWSfP; shshshfp=6e62d1d83949534bb18f96480e1f913e; shshshfpa=211ad900-bac7-8b61-42b3-c82cc7f72fdc-1566537958; shshshfpb=toORyKTnnp3cHkzs0C1fhyw%3D%3D; unpl=V2_ZzNtbUADQkUgXEJSLhsLUWIHFlxLUUtAcVtAXCgeDgY0UEUIclRCFX0URlVnGVsUZwIZXUJcRxJFCEdkexhdBGYGGl9KX3MRdgtGV30cXDVXABJtQ2dDEXIMTld%2fEVQAYQcbVUpWRxdyC0FQSylcDWMzIg0XCxtKGwtHVHwpXARvBBRZR1NFFEUJdlVLUjIEKgMWWkZfQBF9AENSfxBUDWYHEFpBUEcldDhF; __jdc=50436146; __jdv=76161171|cps.youmai.com|t_1000049399_52212741|tuiguang|3e0ade57d3fe4550879d5b79b6c2bbfd|1571191923884; areaId=1; ipLoc-djd=1-2809-0-0; PCSYCityID=CN_110000_110100_110112; sso.jd.com=BJ.943e1d13728f4e6d877524ff7bb98eab; mba_muid=1565925994758990536265; jd.erp.lang=zh_CN; 3AB9D23F7A4B3C9B=PF4UR2DKDPP27JNFFRPGHJ4RFC766TFLJNWB4DUACOE2ESAJOBQ4SGWSQEY7ISGBLY54MRJY4IDYO4HMPXVQQQG67Q; __jd_ref_cls=MLoginRegister_SMSVerificationAppear'
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