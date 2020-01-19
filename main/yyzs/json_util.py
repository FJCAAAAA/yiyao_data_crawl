import json

read_file = 'category.txt'
file = open(read_file)
lines = file.readlines()
count = 0
for line in lines:
    d = json.loads(line)
    first_cate_list = d['results']['items']
    for first_cate in first_cate_list:
        # print(first_cate['id'],first_cate['cnName'])
        if 'childCategoryList' in first_cate:
            child_category_list = first_cate['childCategoryList']
            if child_category_list is not None:
                for child_category in child_category_list:
                    count += 1
                    print(first_cate['id'], first_cate['cnName'], child_category['id'], child_category['cnName'])
        else:
            count += 1
            print(first_cate['id'], first_cate['cnName'])
print(count)
