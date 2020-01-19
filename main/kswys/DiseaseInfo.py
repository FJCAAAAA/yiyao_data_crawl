import requests
import random
import time
from bs4 import BeautifulSoup
import main.kswys.UserAgent

# keshi_name="yixianyan"
# total_page=1
# url="http://www.120ask.com/list/"+keshi_name+"/over/"+str(total_page)
header={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection':'keep-alive',
    'Cookie':'__jsluid=18cd36d8cad4b417fc78b74acf6e8b54; comHealthCloudUserProfileUseTag=42643a921c6b45b6baa8c296ffdbf2ca; UM_distinctid=1696fd863fba0d-05479e111c796c-5e442e19-1fa400-1696fd863fc1be; Hm_lvt_7c2c4ab8a1436c0f67383fe9417819b7=1552359646; TUSHENGSID=TS1552359646560; _ga=GA1.2.628728754.1552359663; _gid=GA1.2.604886045.1552359663; page_keyword=%E5%8E%BB%E5%B9%B45%E6%9C%88%E5%8F%B3%E8%85%BF%E8%84%9A%E8%85%95%E9%9F%A7%E5%B8%A6%E6%8B%89%E4%BC%A4%E8%BF%87; CNZZDATA30036369=cnzz_eid%3D937902712-1552359625-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1552358799; Hm_lpvt_7c2c4ab8a1436c0f67383fe9417819b7=1552361637',
    'Host':'www.120ask.com',
    'Pragma':'no-cache',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':random.choice(main.kswys.UserAgent.pcUserAgent)
}

def get_total_pages(jb_url):
    '''
    获取该科室疾病对应的总页码
    :param jb_url: 疾病url
    :return: 总共页码数
    '''
    list_html=requests.get(url=jb_url,headers=header)
    list_soup = BeautifulSoup(list_html.text,'lxml')
    total_pages=0
    # page_tags=list_soup.find_all('div',attrs={'class':'clears h-page'})
    page_tags=list_soup.find_all('a',attrs={'target':'_self'})
    for page_tag in page_tags:
        if page_tag.get_text()=='最后一页':
            total_pages=page_tag['href'].split('/')[-2]
    return total_pages

def get_disease_url(jb_url):
    '''
    获取相应病情单个列表页的详情页url集
    :param jb_url: 访问列表页的url
    :return: 相应病情的详情页url集
    '''
    list=[]
    list_html=requests.get(url=jb_url,headers=header)
    list_soup = BeautifulSoup(list_html.text,'lxml')
    taglist = list_soup.find_all('a',attrs={'class':'q-quename'})
    for tag in taglist:
        bq_url='http:'+tag['href']
        list.append(bq_url)
    return list

def get_disease_description(disease_url):
    '''
    获取详情页的病情描述
    :param disease_url:访问详情页的url
    :return:返回一个详情数据字典
    '''
    dict={}
    detail_html=requests.get(url=disease_url,headers=header)
    detail_soup = BeautifulSoup(detail_html.text,'lxml')
    taglist = detail_soup.find_all('div',attrs={'class':'b_askbox'})
    for tag in taglist:
        try:
            title=tag.find('h1').get_text()
            dict["title"]=title
            gender_age=tag.find_all('div',attrs={'class':'b_askab1'})[0].get_text().strip().split(' ')
            dict["gender"]=gender_age[0]
            dict["age"]=gender_age[2]
            detail=tag.find_all('p',attrs={'class':'crazy_new'})[0].get_text().split('健康咨询描述：')[1].strip()
            dict["detail"]=detail
        except(IndexError,UnicodeEncodeError):
            print(IndexError,UnicodeEncodeError)
    return dict

# def write_to_excel(dict,row):
#     workbook = xlwt.Workbook(encoding = 'ascii')
#     worksheet = workbook.add_sheet('Test')
#     worksheet.write(row, 0, label = keshi_name)
#     worksheet.write(row, 1, label = dict['gender'])
#     worksheet.write(row, 2, label = dict['age'])
#     worksheet.write(row, 3, label = dict['title'])
#     worksheet.write(row, 4, label = dict['detail'])
#     workbook.save(keshi_name+'.xls')

def write_to_txt(dict,write_path):
    '''
    将数据写入txt文本
    :param dict: 字典数据
    :return:
    '''
    try:
        file = open(write_path,'a',encoding='utf-8')
        file.write(dict['class']+'\t'+dict['gender']+'\t'+dict['age']+'\t'+dict['detail']+'\n')
    except(UnicodeEncodeError,KeyError,IOError,RuntimeError,IndexError):
        return

def read_from_txt_and_visit_url(path):
    fi=open(path)
    lines=fi.readlines()
    for line in lines:
        lis=line.split('\t')
        disease_url=lis[0]
        dissease_name=lis[1].strip()
        over_disease_url=disease_url+"over/"
        write_path=dissease_name+'.txt'
        total_page=get_total_pages(over_disease_url)
        for page in range(start_page,int(total_page)+1):
            over_disease_url_page=over_disease_url+str(page)
            print(over_disease_url_page)
            disease_url_list=get_disease_url(over_disease_url_page)
            for disease_url in disease_url_list:
                dict=get_disease_description(disease_url)
                dict['class']=dissease_name
                try:
                    print(dict)
                except(UnicodeEncodeError):
                    print(UnicodeEncodeError)
                write_to_txt(dict,write_path)
                # break
                time.sleep(0.1)
            # break

def main():
    read_path='disease.txt'

    read_from_txt_and_visit_url(read_path)

if __name__=='__main__':
    start_page=1
    main()




