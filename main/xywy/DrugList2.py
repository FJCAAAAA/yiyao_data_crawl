# coding=gbk

import requests
from bs4 import BeautifulSoup
import bs4
import main.xywy.UserAgent
import random
import time
import json

header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'clientac=1553155378582482733; visit_dt=2019-2-21; countNum=1; wksc-20480=BOABBOAKFAAA; UM_distinctid=1699f46970f141-011b77d30b1ed4-5e442e19-1fa400-1699f4697102d5; PHPSESSID=im6f5lcioofcotnn3ncqqdvbl5; city=%B1%B1%BE%A9%CA%D0; __gg_t_city=%B1%B1%BE%A9%CA%D0; __gg_t_loc=%B1%B1%BE%A9%CA%D0; city_xywy_ad=北京市; __gg_city=北京市; beijing=true; baidu_referer=0; drug_visitor_logs=48930%2C; CNZZDATA30081008=cnzz_eid%3D1913135878-1553153171-http%253A%252F%252Fwww.xywy.com%252F%26ntime%3D1553152025; ajsDataSession=1553155378582495105@11@1553157343@2@http%253A%252F%252Fyao.xywy.com%252Fclass%252F4-0-0-1-0-2.htm@http%253A%252F%252Fyao.xywy.com%252Fclass%252F4-0-0-1-0-1.htm; tj_lastUrl=http%3A//yao.xywy.com/class/4-0-0-1-0-2.htm; tj_lastUrl_time=1553157343981',
    'Host':'yao.xywy.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':random.choice(main.xywy.UserAgent.pcUserAgent)
}

# url='http://yao.xywy.com/goods/48930.htm'
# html=requests.get(url=url)
# soup = BeautifulSoup(html.text,'lxml')

main_url='http://yao.xywy.com'
def insertion_sort(old_list):
    n=len(old_list)
    k=0
    for i in range(1,n):
        temp=old_list[i]
        j=i
        while j>0 and temp<old_list[j-1]:
            old_list[j]=old_list[j-1]
            j=j-1
        old_list[j]=temp
    return old_list

def write_to_json(dict):
    '''
    将数据写入txt文本
    :param dict: 字典数据
    :return:
    '''
    try:
        file = open(write_path,'a',encoding='utf-8')
        json_array = json.dumps(dict,ensure_ascii=False)
        file.write(json_array+'\n')
        file.flush()
        print(json_array)
    except(UnicodeEncodeError,KeyError,IOError,RuntimeError,IndexError):
        return

def list_to_dict(trade_introduce_list):
    dict={}
    for trade_introduce in trade_introduce_list:
        arr=trade_introduce.split('：')
        if len(arr)==2:
            key=arr[0].replace(',','')
            dict[key]=arr[1]
        elif len(arr)>2:
            key=arr[0].replace(',','')
            v=arr[1:]
            value='：'.join(v)
            dict[key]=value
    return dict

def get_sku_detail_url(list_sku_url):
    for sku_url in list_sku_url:
        url=main_url+sku_url
        try:
            html=requests.get(url=url)
            soup = BeautifulSoup(html.text,'lxml')
            tag=soup.find('div',attrs={'class':'d-info fl ml20 mt20'})
            trade_introduce_list=[]
            specification_list=[]
            try:
                drug_title=tag.find('h2',attrs={'class':'fn c3 f18'})
                print(type(drug_title))
                trade_introduce_list.append('商品名称：'+drug_title.get_text())
                property=tag.find('div',attrs={'class':'d-info-dl mt20'}).find_all('dl',attrs={'class':'clearfix'})
                if property is not None:
                    for s in property:
                        content=s.find('div',attrs={'class':'fl'})
                        if content is not None:
                            pzwh_name=content.get_text()
                            numbox=s.find('div',attrs={'class':'phonebox fl pz-box'}).find_all('b')
                            dict={}
                            for num in numbox:
                                num_key=int(num['style'].split('-')[1].split('px')[0])
                                dict[num_key]=num.get_text()
                            list=sorted(dict.keys(),reverse=True)
                            pzwh_num=''
                            for li in list:
                                value=dict[li]
                                pzwh_num=pzwh_num+value
                            pzwh=pzwh_name+pzwh_num
                            trade_introduce_list.append(pzwh)
                        else:
                            other_content=s.get_text().strip().replace('\u200b', '').replace('\r\n', '').replace('\n', '')
                            if other_content.startswith('相关疾病'):
                                str=[]
                                words=s.find_all('a')
                                for word in words:
                                    str.append(word.get_text())
                                other_content=','.join(str)
                                other_content='相关疾病：'+other_content
                            if other_content is not None:
                                trade_introduce_list.append(other_content)
                spec_list=soup.find('div',attrs={'class':'d-direction'}).find_all('p')
                if spec_list is not None:
                    for spec in spec_list:
                        general_spec=spec.get_text().strip().replace('\u200b', '').replace(' ', ',').replace('\r\n', '').replace('\n', '')
                        trade_introduce_list.append(general_spec)
            except(AttributeError,UnicodeDecodeError,IndexError):
                print(AttributeError)
                # trade_introduce_list.append('商品名称：'+url)
                # file = open(unanalyse_path,'a',encoding='utf-8')
                # file.write(url+'\n')
                # file.flush()
            trade_introduce_dict=list_to_dict(trade_introduce_list)
            write_to_json(trade_introduce_dict)
        except(UnicodeDecodeError):
            print(UnicodeDecodeError)





'''
def get_cur_pages():
    pages=0
    url=main_url+'/class/4-0-0-1-0-1.htm'
    print(url)
    html=requests.get(url=url)
    soup = BeautifulSoup(html.text,'lxml')
    page_tags=soup.find('div',attrs={'id':'flip'}).find('a')
    print(page_tags)
    return pages
'''

def get_sku_list_url(read_path):
    fi=open(read_path)
    lines=fi.readlines()
    for line in lines:
        infos=line.split(',')
        sub_url=infos[0].replace('1.htm','')
        total_pages=infos[1]
        for page in range(start_page,int(total_pages)+1):
            list_sku_url=[]
            url=main_url+sub_url+str(page)+'.htm'
            html=requests.get(url=url)
            soup = BeautifulSoup(html.text,'lxml')
            tag_list=soup.find_all('div',attrs={'class':'h-drugs-hd clearfix'})
            for tag in tag_list:
                sku_cate_url=tag.a['href']
                list_sku_url.append(sku_cate_url)
                # print(sku_cate_url)
            print(url)
            get_sku_detail_url(list_sku_url)
            time.sleep(2)



def get_all_sku_cate_url():
    list_sku_cate_url=[]
    html=requests.get(url=main_url)
    soup = BeautifulSoup(html.text,'lxml')
    tag_list=soup.find_all('dl',attrs={'class':'item_classly'})
    for tag in tag_list:
        sku_cate_url=tag.a['href']
        list_sku_cate_url.append(sku_cate_url)
        print(sku_cate_url)
    return list_sku_cate_url

def main():
    # #获取药品分类的url
    # get_all_sku_cate_url()
    #获取药品的url
    get_sku_list_url(read_path)
    # #获取药品的属性信息
    # trade_introduce_dict=get_sku_detail_url()
    # #将数据写出成json格式
    # write_to_json(trade_introduce_dict)

if __name__ == '__main__':
    unanalyse_path='unanalyse.txt'
    write_path='ylqx.txt'
    read_path='ylqx_cate'
    start_page=11
    main()