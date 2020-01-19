# coding:utf-8

import os
xiaoquDir='F:\\anjuke\\福建\\'
list = os.listdir(xiaoquDir)
for i in range(0,len(list)):
    path=os.path.join(xiaoquDir,list[i])
    new_path=os.path.join(xiaoquDir,'new_'+list[i])
    if os.path.isfile(path):
        quyu_name=os.path.basename(path)
        quyu_file=open(path,encoding='utf-8')
        xiaoqu_lines=quyu_file.readlines()
        for xiaoqu_line in xiaoqu_lines:
            xiaoqu=xiaoqu_line.rstrip('\n')
            # print(xiaoqu)
            one_index=xiaoqu.find('（')
            two_index=xiaoqu.find('(')
            if one_index==-1 and two_index==-1:
                new_xiaoqu=xiaoqu
            else:
                if one_index!=-1:
                    new_xiaoqu=xiaoqu[0:one_index]
                else:
                    new_xiaoqu=xiaoqu[0:two_index]
            file = open(new_path,'a')
            file.write(new_xiaoqu+'\n')