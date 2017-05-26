#!/bin/bash

if [ $1 ]
then
    path=/version/new
    filePath=/version/new/$1
    if [ -d $filePath ]
    then
        echo '正在获取新代码'
      	cd $filePath
      	git add *
      	git stash
      	git pull
    else
      	cd $path
      	echo '正在抓取项目代码'
      	git clone -b master git@192.168.1.240:Ivone/$1
    fi
    echo '正在进行文件比对 ...'
    cd /home/script/vlib
    python compare.py $1
else
    echo '未输入项目名，请输入后重试'
fi
