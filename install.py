#encoding=utf8

import sys,os,filecmp,re,time
#需要安装tqdm插件
from tqdm import tqdm

def create(p,floder):
    #测试机文件路径
    locate = '/version/new/%s'%(p)
    note = open('/home/script/vlib/package/%s/notes.sh'%(str(floder)),'a+')
    note.write('#!/bin/bash \n')
    #测试机文件路径
    for parent,dirname,filenames in tqdm(os.walk(locate)):
        for filename in filenames:
            filePath = os.path.join(parent,filename)
            if not re.search(r'.git',str(filePath)):
                relatively = filePath.split('%s'%(p))
                os.system('cp %s /home/script/vlib/package/%s'%(str(filePath),str(floder)))
                note.write('cp %s %s \n'%(str(filename),str(relatively[1])))
    note.flush()
    note.close()
    print "正在生成安装包 ..."
    os.system('tar zcvf /home/script/vlib/install/%s.tar.gz ./package/%s'%(str(floder),str(floder)))
    print "安装包已生成，位置： /home/script/vlib/install/%s.tar.gz"%(str(floder))



if __name__ == '__main__':
    try:
        #获取项目名参数
        project = sys.argv[1]
        now = time.time()
        os.system("mkdir ./package/%s-%s"%(str(project),str(now)))
        os.system("touch ./package/%s-%s/notes.sh"%(str(project),str(now)))
        floder = "%s-%s"%(str(project),str(now))
    except:
        print "未输入项目名！程序结束。"
    create(str(project),str(floder))
