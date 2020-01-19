
def filter_len_to_short(path):
    null_count=0
    file=open(path,encoding="utf-8")
    lines=file.readlines()
    for line in lines:
        try:
            if len(line)<100:
                null_count+=1
                print(line)
            else:
                file = open(write_path,'a',encoding='utf-8')
                file.write(line)
                file.flush()
        except(UnicodeEncodeError):
            print(UnicodeEncodeError)
    print(null_count)

if __name__ == '__main__':
    read_path=r'zxyp.txt'
    write_path=r'zxyp_n.txt'
    filter_len_to_short(read_path)
