
import random
from yiyao_data_crawl.main.common.WebUtils import *
from yiyao_data_crawl.main.common.UserAgent import pcUserAgent

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': random.choice(pcUserAgent),
    'Cookie': 'UM_distinctid=16ae421f61a1f5-06a46bc970e867-353166-1fa400-16ae421f61ba18; '
              'CNZZDATA30033562=cnzz_eid%3D1030876382-1558601275-%26ntime%3D1561095027; '
              'Hm_lvt_224d1dc4be80509b8817ce60aca82160=1558605592,1559135410,1561096497; '
              'Hm_lvt_570f165bc826f5c245327416e244a9c5=1558605592,1559135410,1561096497,1561096596; '
              'CNZZDATA30033500=cnzz_eid%3D171731265-1558603315-%26ntime%3D1561098489;'
              ' Hm_lpvt_570f165bc826f5c245327416e244a9c5=1561099398; '
              'Hm_lpvt_224d1dc4be80509b8817ce60aca82160=1561099398',
    'Referer': 'http://jb.9939.com/jbzz/jingbu/',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'close',
    'Host': 'jb.9939.com'
}

item_dic = {'发病部位': '部位', '别名': '别名', '多发人群': '人群'}


def main():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
    file.close()
    for line in lines:
        line_sp = line.split("\t")
        url = "http://jb.9939.com/" + line_sp[1].strip()

        num = 1
        while not get_page(url, 0):
            if num > 5:
                write_str_to_txt(line + "\n", write_fail_path)
                print(url, "查询失败")
                break

            print("\n\n页面加载失败，5s分钟后重试", url)
            time.sleep(5)

            num = num + 1
        time.sleep(1)


def get_page(url, times):
    jj_soup = get_soup(url+'jianjie', times, header)
    if not jj_soup:
        return 0
    name = jj_soup.find('div', class_='art_s').text.split('>').pop().strip()
    result = {'疾病': name}

    jj_items_div = jj_soup.find('div', class_='protex')
    if jj_items_div:
        for p in jj_items_div.find_all('p'):
            title = p.text.split('：')[0].strip()
            if title not in item_dic.keys():
                continue

            ctt = '||'.join(filter(None, re.split('[\\s]', p.text.split('：')[1])))
            result[item_dic[title]] = ctt

    ke_div = jj_soup.find('div', class_='aknol')
    if ke_div:
        item_for(result, '科室', ke_div.find('p').find_all('a'), 'list')

    med_div = jj_soup.find('div', class_='refl')
    if med_div:
        item_for(result, '药品', med_div.find_all('a'), 'list')

    gai_div = jj_soup.find('div', class_='bshare')
    if gai_div:
        item_for(result, '概述', gai_div.find_all('p'), 'str')

    zz_soup = get_soup(url+'zz', times, header)
    if zz_soup:
        zz_div = zz_soup.find('div', class_='spread')
        if zz_div:
            item_for(result, '典型症状', zz_div.find_all('a', title=True), 'list')
            item_for(result, '症状内容', zz_div.find_all('p', style=True), 'str')

    yf_soup = get_soup(url+'yf', times, header)
    if yf_soup:
        yf_div = yf_soup.find('div', class_='spread')
        if yf_div:
            item_for(result, '预防', yf_div.find_all('p', style=True), 'str')

    jc_soup = get_soup(url+'lcjc', times, header)
    if jc_soup:
        jc_div = jc_soup.find('div', class_='spread')
        if jc_div:
            item_for(result, '检查项目', jc_div.find_all('a', style=True), 'list')
            item_for(result, '检查内容', jc_div.find_all('p', style=True), 'str')

    jb_soup = get_soup(url+'jb', times, header)
    if jb_soup:
        jb_div = jb_soup.find('div', class_='spread')
        if jb_div:
            item_for(result, '鉴别', jb_div.find_all('p', style=True), 'str')

    zl_soup = get_soup(url+'zl', times, header)
    if zl_soup:
        zl_div = zl_soup.find('div', class_='spread')
        if zl_div:
            zlfs = zl_div.find('p')
            if zlfs:
                result['治疗方式'] = '||'.join(filter(None, re.split('[\\s,，、]', zlfs.text)))
            item_for(result, '治疗内容', zl_div.find_all('p', class_='spea'), 'str')

    hl_soup = get_soup(url+'yshl', times, header)
    if hl_soup:
        hl_div = hl_soup.find('div', class_='spread')
        if hl_div:
            item_for(result, '护理', hl_div.find_all('p', style=True), 'str')

    bfz_soup = get_soup(url+'bfz', times, header)
    if bfz_soup:
        bfz_div = bfz_soup.find('div', class_='spread')
        if bfz_div:
            item_for(result, '并发症', bfz_div.find_all('p', class_='spea'), 'str')

    write_json_to_txt(result, write_dis_path)
    print(name, '成功')
    return 1


if __name__ == '__main__':
    list_page_path = 'txt/ListDis9939.txt'
    write_dis_path = 'txt/detail/Dis9939.txt'
    write_fail_path = 'txt/ListFail9939.txt'

    main()




