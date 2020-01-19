# coding=gbk
import requests
import time
import json
import math
import random
import main.yyzs.UserAgent

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'User-Agent': random.choice(main.yyzs.UserAgent.appUserAgent)
}
sessionId = 'eyJhcHBJZCI6MTI2MTgyODY1NywiZHh5VXNlck5hbWUiOiJkeHlfYWJ6M2ZucTgiLCJub25jZSI6IllzRE9RRFZGSXdTY1NkZnAiLCJwcm9maWxlSWQiOjQ4ODEyMjAwLCJzaWduIjoiZDI0M2E5ZWRhYzA2Mzg3MGFhMjZjNzkzZWNlNWY3MTIzMzE5Njk3ZiIsInNpbXVpZCI6NjY3NTE3NTA5NTY0MTY5NDI4OSwidGVhbUlkIjo0ODUsInRpbWVzdGFtcCI6MTU1NzcxMjEzNH0'
headers3 = {
    'charset': "utf-8",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json",
    'Connection': "Keep-Alive",
    'Host': "drugs.dxy.cn",
    'dxy-wxapp-auth-token': "eyJhcHBJZCI6MTI2MTgyODY1NywiZHh5VXNlck5hbWUiOiJkeHlfMHcybzI3cCIsIm5vbmNlIjoidkRMcDB5djVyMDNERWplZSIsInByb2ZpbGVJZCI6NDg2NjA4MTcsInNpZ24iOiJjNjE5ZmY1NjUwYjQ1YjIxY2Y1ZmU1ZWE0ZGFkODAxMWVjZTc3NzNiIiwic2ltdWlkIjo2NjczMzIwNjIzMjUyMTUwNDQ0LCJ0ZWFtSWQiOjQ4NSwidGltZXN0YW1wIjoxNTUzNzUzNzczfQ"
}


# response = requests.request("POST", url, data=payload, headers=headers,verify=False)
#
# print(response.text)
def get_cate_ids_info():
    cate_list_url = 'https://drugs.dxy.cn/api/open/category/list?sessionId=' + sessionId
    json_data = requests.get(cate_list_url, headers=headers, verify=False)
    print(json_data.text)


def read_cateid_from_category_file(read_category_path):
    second_cate = []
    file = open(read_category_path)
    lines = file.readlines()
    for line in lines:
        words = line.split(' ')
        li = list(words)
        second_cate.append(li)
    return second_cate


def write_to_txt(category_id_info, write_category_pages_path):
    try:
        file = open(write_category_pages_path, 'a', encoding='utf-8')
        str = '|'.join(category_id_info).replace('\n', '')
        print(str)
        file.write(str + '\n')
        file.flush()
    except():
        print('数据未写入' + category_id_info)


def get_drug_ids_with_pages_info():
    category_id_info_list = read_cateid_from_category_file(read_category_path)
    for category_id_info in category_id_info_list:
        if len(category_id_info) == 4:
            category_id = category_id_info[2]
            # print(category_id)
            # category_id=1001
            page = 1
            drug_list_url = 'https://drugs.dxy.cn/api/open/category/drug?sessionId=' + sessionId + '&categoryId=' + str(
                category_id) + '&page=' + str(page)
            print(drug_list_url)
            json_data = requests.get(drug_list_url, headers=headers, verify=False)
            info = json.loads(json_data.text)
            results = info['results']
            if 'pageBean' in results:
                page_bean = results['pageBean']
                total_count = page_bean['totalCount']
                page_size = page_bean['pageSize']
                total_pages = math.ceil(int(total_count) / int(page_size))
                category_id_info.append(str(total_count))
                category_id_info.append(str(total_pages))
        write_to_txt(category_id_info, write_category_pages_path)
        time.sleep(0.5)


def get_drug_ids_info():
    file = open(write_category_pages_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        words = line.split('|')
        li = list(words)
        if len(li) == 6 and li[5] != 0:
            category_id = li[2]
            pages = li[5]
            int_page = 1
            for page in range(int_page, int(pages) + 1):
                drug_list_url = 'https://drugs.dxy.cn/api/open/category/drug?sessionId=' + sessionId + '&categoryId=' + str(
                    category_id) + '&page=' + str(page)
                print(drug_list_url)
                json_data = requests.get(drug_list_url, headers=headers, verify=False)
                info = json.loads(json_data.text)
                info['categoryId'] = category_id
                file = open(write_drug_ids_path, 'a', encoding='utf-8')
                json_array = json.dumps(info, ensure_ascii=False)
                file.write(json_array + '\n')
                file.flush()
                # print(info)
                # items=info['results']['items']
                # file=open(write_drug_ids_path,'a',encoding='utf-8')
                # for item in items:
                #     file.write(item+'\n')
                #     file.flush()
                #     print(item)
                time.sleep(1)


def get_drug_detail_info():
    url = 'https://drugs.dxy.cn/api/v2/detail'
    file = open(write_drug_ids_path, encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        json_data = json.loads(line)
        category_id = json_data['categoryId']
        drug_ids_info = json_data['results']['items']
        print('categoryId is:' + str(json_data['categoryId']) + ',and pageNo is:' + str(
            json_data['results']['pageBean']['pageNo']))
        for drug_id_info in drug_ids_info:
            drug_id = drug_id_info['id']
            show_name = drug_id_info['showName']
            company_name = drug_id_info['companyName']
            print(drug_id)
            payload = 'wxxcx=true&sessionId=' + sessionId + '&category=' + str(2) + '&id=' + str(drug_id)
            json_data_detail = requests.request("POST", url, data=payload, headers=headers, verify=False)
            dict_data_detail = json.loads(json_data_detail.text)
            if 'error' in dict_data_detail:
                print("查询次数过多")
                exit(1)
            else:
                dict_data_detail['categoryId'] = category_id
                dict_data_detail['drugId'] = drug_id
                dict_data_detail['showName'] = show_name
                dict_data_detail['companyName'] = company_name
                json_data_all = json.dumps(dict_data_detail, ensure_ascii=False)
                try:
                    file = open(write_drug_detail_path, 'a', encoding='utf-8')
                    file.write(json_data_all + '\n')
                    file.flush()
                    print('write success')
                except:
                    file = open(error_path, 'a', encoding='utf-8')
                    file.write(str(drug_id) + '\n')
                    file.flush()
                    print('error')
                time.sleep(1)


def main():
    # # 获取一，二级药品分类信息（id,name）
    # get_cate_ids_info()
    # # 获取当前分类下的总页数
    # get_drug_ids_with_pages_info()
    # # 获取药品ids
    # get_drug_ids_info()
    # 获取药品详情信息
    get_drug_detail_info()


if __name__ == '__main__':
    read_category_path = 'category_txt.txt'
    write_category_pages_path = 'category_pages.txt'
    write_drug_ids_path = 'drug_ids.txt'
    write_drug_detail_path = 'drug_detail.txt'
    error_path = 'error.txt'
    main()
