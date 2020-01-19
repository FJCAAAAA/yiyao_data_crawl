
import random
from main.common.WebUtils import *
from main.common.UserAgent import pcUserAgent

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


def main():

    file = open(list_page_path, encoding='utf-8')
    lines = file.readlines()
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
    soup = get_soup(url, times, header)
    if not soup:
        return 0

    name = soup.find('div', class_='art_s').text.split('>').pop().strip()
    ul = soup.find('ul', class_='dissy')
    if ul:
        item_list = ul.find_all('li', class_='with_01')
        if item_list:
            diss = list()
            for item in item_list:
                diss.append(item.text.strip())

            write_json_to_txt({'症状': name, '可能疾病': '||'.join(diss)}, write_sym_path)
            print(name, "写入成功")

    else:
        print(url, "未读取到列表")
        write_str_to_txt(name+'\t'+url, write_fail_path)

    return 1


if __name__ == '__main__':
    list_page_path = 'txt/ListSym9939.txt'
    write_sym_path = 'txt/detail/Sym9939.txt'
    write_fail_path = 'txt/ListFail9939.txt'

    main()




