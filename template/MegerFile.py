
import os


meger_dir='F:\\anjuke\\福建\\泉州'
target_path='F:\\anjuke\\福建\\泉州\\泉州.txt'
list = os.listdir(meger_dir)
for i in range(0,len(list)):
    path=os.path.join(meger_dir,list[i])
    fi=open(path)
    lines=fi.readlines()
    for line in lines:
        target_file=open(target_path,'a',encoding='utf-8')
        target_file.write(line)
        target_file.flush()
