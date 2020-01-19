# coding:utf-8

import requests
import random
import os
import main.python.fjn.Proxies
import main.python.fjn.UserAgent
from bs4 import BeautifulSoup

# url = 'https://yun.kujiale.com/dds/api/c/designdata/3FO4M4B185PK?20180620211509=1'
# url2='https://www.kujiale.com/api/huxing/3FO4LH209NTD/create'
#
# ie=random.choice(main.python.fjn.UserAgent.pcUserAgent)
# print(ie)
# headers={
#     'Cookie':'usersource=www.baidu.com; qhdi=5fb347b5791c11e8bd8315e45db47465; KSESSIONID=5fb320a4791c11e8bd83b7f695c5064b; gr_user_id=b47f3fc0-2628-40ba-9a3f-0131fedff6b4; _ga=GA1.2.1549018552.1530002343; _gid=GA1.2.721122369.1530002343; ktrackerid=61120afd-d3d5-434e-b0d9-68266606ce68; lastEnteredTool=h5diy; landingpageurl=https%3A%2F%2Fwww.kujiale.com%2Fhuxing%2Fflash%3Fkpm%3D9V8.PqZ.7d22134.1530096088386; fromsrcurl=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DA8P2ZKEz01tG_zpSoZOXZb_jJqpBNPp5UaxD3jUEkHiJGYAsWRtt6Y_fiuKsZXA9%26wd%3D%26eqid%3Dd8af11ae0001e8e5000000035b3458c0; qhssokey=3FO4JNLKAA5ISOI8S0KE; qhssokeyid=SOI8S0KE; qhssokeycheck=3FO4JNLKAA5I; gr_cs1_a0e22c46-1d3c-42d9-bc65-87781f74ebc7=userId%3A3FO4JNLKAA5I; gr_session_id_a4a13a22eb51522b=a0e22c46-1d3c-42d9-bc65-87781f74ebc7_true; Hm_lvt_bd8fd4c378d7721976f466053bd4a855=1530002343,1530086877,1530157254,1530171394; kjl_usercityid=36; designer_called_level_api_3FO4JNLKAA5I=true; DIYSERVERS=1; Hm_lpvt_bd8fd4c378d7721976f466053bd4a855=1530173032; _gat=1; JSESSIONID=187nietvfs95y1j2onjwlbtu22'}
#
# # data=requests.get(url=url,headers=headers,proxies=main.python.fjn.Proxies.proxies).text
# data=requests.post(url=url2,headers=headers,proxies=main.python.fjn.Proxies.proxies).text
# print(data)

def get_new_id(huxing_id,times):
    create_id_url='https://www.kujiale.com/api/huxing/'+huxing_id+'/create'
    new_create_id=requests.post(url=create_id_url,headers=headers,proxies=main.python.fjn.Proxies.proxies).text
    get_data(huxing_id,new_create_id,times)

def get_data(huxing_id,new_create_id,times):
    data_url = 'https://yun.kujiale.com/dds/api/c/designdata/'+new_create_id+'?20180620211509=1'
    data=requests.get(url=data_url,headers=headers,proxies=main.python.fjn.Proxies.proxies).text
    print('NO'+str(times)+'\t'+huxing_id+'===='+new_create_id)
    kujialePath=kujialeDir+huxing_id+'.txt'
    kujialeFile=open(kujialePath,'w',encoding='utf-8')
    kujialeFile.write(data)
    kujialeFile.flush()
    # print(data)

def get_huxing_id(city_name,city_url,house):
    times=0
    for page in range(1,14):
        if house.strip()=='':
            huxing_url='https:'+city_url+'/'+str(page)
        else:
            huxing_url='https:'+city_url+'-'+house+'/'+str(page)
        session = requests.session()
        html = session.get(huxing_url)
        soup = BeautifulSoup(html.text,'lxml')

        #匹配带有class属性的li标签
        taglist = soup.find_all('li',attrs={'class':'tpl-huxingtu'})
        for lilist in taglist:
            times=times+1
            dataId=(lilist['data-id'])
            get_new_id(dataId,times)

headers={
        'Host':'yun.kujiale.com',
        'Connection':'keep-alive',
        'Pragma':'no-cache',
        'Cache-Control':'no-cache',
        'Accept':'text/plain,*',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'x-tool-name':'diy',
        # 'Referer':'https://yun.kujiale.com/tool/h5/diy?designid=3FO4M7PI59IW&em=0',
        'Accept-Encoding':'gzip,deflate,br',
        'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cookie':'usersource=www.baidu.com; qhdi=5fb347b5791c11e8bd8315e45db47465; KSESSIONID=5fb320a4791c11e8bd83b7f695c5064b; gr_user_id=b47f3fc0-2628-40ba-9a3f-0131fedff6b4; _ga=GA1.2.1549018552.1530002343; _gid=GA1.2.721122369.1530002343; ktrackerid=61120afd-d3d5-434e-b0d9-68266606ce68; lastEnteredTool=h5diy; landingpageurl=https%3A%2F%2Fwww.kujiale.com%2Fhuxing%2Fflash%3Fkpm%3D9V8.PqZ.7d22134.1530096088386; fromsrcurl=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DA8P2ZKEz01tG_zpSoZOXZb_jJqpBNPp5UaxD3jUEkHiJGYAsWRtt6Y_fiuKsZXA9%26wd%3D%26eqid%3Dd8af11ae0001e8e5000000035b3458c0; qhssokey=3FO4JNLKAA5ISOI8S0KE; qhssokeyid=SOI8S0KE; qhssokeycheck=3FO4JNLKAA5I; gr_cs1_a0e22c46-1d3c-42d9-bc65-87781f74ebc7=userId%3A3FO4JNLKAA5I; gr_session_id_a4a13a22eb51522b=a0e22c46-1d3c-42d9-bc65-87781f74ebc7_true; Hm_lvt_bd8fd4c378d7721976f466053bd4a855=1530002343,1530086877,1530157254,1530171394; kjl_usercityid=36; designer_called_level_api_3FO4JNLKAA5I=true; DIYSERVERS=1; Hm_lpvt_bd8fd4c378d7721976f466053bd4a855=1530173032; _gat=1; JSESSIONID=187nietvfs95y1j2onjwlbtu22'
        # 'Cookie':'qhdi=32cdcba078ed11e8bd8775292f12014b; '
        #          'KSESSIONID=32cdcb9f78ed11e8bd87510fb5f5e01e; '
        #          'gr_user_id=178444a9-1530-4442-ae7b-d8cca60cc1b1; '
        #          '_ga=GA1.2.633225660.1529982082; '
        #          '_gid=GA1.2.1477558245.1529982082; '
        #          'usersource=open.weixin.qq.com; '
        #          'DIYSERVERS=1; '
        #          'lastEnteredTool=h5diy; '
        #          'Hm_lvt_bd8fd4c378d7721976f466053bd4a855=1529999412; '
        #          'landingpageurl=https%3A%2F%2Fyun.kujiale.com%2Ftool%2Fh5%2Fdiy%3Fdesignid%3D3FO4M79F7M0E%26em%3D0; '
        #          'kjl_usercityid=36; '
        #          'gr_cs1_3cdbaf4d-26b1-452f-b16a-561d17409579=userId%3A3FO4K9OJ249V; '
        #          'gr_session_id_a4a13a22eb51522b=3cdbaf4d-26b1-452f-b16a-561d17409579_true; '
        #          'Hm_lpvt_bd8fd4c378d7721976f466053bd4a855=1530193429; '
        #          '_gat=1; JSESSIONID=1x84n9mq9fgu540a09qnx65n; '
        #          'qhdi=32cdcba078ed11e8bd8775292f12014b; '
        #          'KSESSIONID=32cdcb9f78ed11e8bd87510fb5f5e01e; '
        #          'gr_user_id=178444a9-1530-4442-ae7b-d8cca60cc1b1; '
        #          '_ga=GA1.2.633225660.1529982082; '
        #          '_gid=GA1.2.1477558245.1529982082; '
        #          'usersource=open.weixin.qq.com; '
        #          'DIYSERVERS=1; '
        #          'lastEnteredTool=h5diy; '
        #          'Hm_lvt_bd8fd4c378d7721976f466053bd4a855=1529999412; '
        #          'landingpageurl=https%3A%2F%2Fyun.kujiale.com%2Ftool%2Fh5%2Fdiy%3Fdesignid%3D3FO4M79F7M0E%26em%3D0; '
        #          'kjl_usercityid=36; '
        #          'gr_cs1_3cdbaf4d-26b1-452f-b16a-561d17409579=userId%3A3FO4K9OJ249V; '
        #          'gr_session_id_a4a13a22eb51522b=3cdbaf4d-26b1-452f-b16a-561d17409579_true; '
        #          'Hm_lpvt_bd8fd4c378d7721976f466053bd4a855=1530193687; '
        #          '_gat=1; '
        #          'JSESSIONID=xpcg287vobtdihztlczqel4s'
}

province_name='福建'
cityDir='F:\\kujialeCity\\'+province_name+'\\'
anjukeDir='F:\\anjuke\\'+province_name+'\\'
cityList = os.listdir(anjukeDir)
for i in range(0,len(cityList)):
    house_path=os.path.join(anjukeDir,cityList[i])
    if os.path.isfile(house_path):
        house_city_name=os.path.basename(house_path).split('.')[0]
        house_file=open(house_path)
        house_lines=house_file.readlines()
        for house_line in house_lines:
            house=house_line.rstrip('\n')
            print(house_city_name+' '+house)

            files=os.listdir(cityDir)
            for fi in files:
                name_file=os.path.basename(fi)
                city_name=name_file.split('.')[0]
                # if not city_name.startswith('全部'):
                if (city_name==house_city_name):
                    kujialeDir='F:\\kujialeData\\'+province_name+'\\'+house_city_name+'\\'
                    if not os.path.exists(kujialeDir):
                        os.makedirs(kujialeDir)
                    f=open(cityDir+name_file)
                    city_url=f.read()
                    get_huxing_id(city_name,city_url,house)


