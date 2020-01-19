def read_from_txt(path):
    fi=open(path)
    lines=fi.readlines()
    for line in lines:
        lis=line.split('\t')
        url=lis[0]
        name=lis[1]
        print(url,name)

path='disease.txt'
read_from_txt(path)