#!/bin/bash

:<<!
alpha1说明：
git直接获取代码进行部署。
ps：只能获取git上面的代码，最好将配置文件修改好直接上传。
alpha2说明：
添加了自动生成nginx的vhosts的功能，并且会马上生效

@param:string，只有一个参数
@author:Ivone
@version:alpha 2
@time:2016-12-29
!

#拼接路径
filePath="/home/website/$1/"
#echo $filePath

#判断路径是否存在
if [ -d $filePath ]
then
    echo "程序开始执行,请稍等 ..."
    #进入路径，并且执行代码更新
    cd $filePath
    git add * && git stash
    git pull
    echo "程序执行结束"
else
    #从git服务器上克隆项目代码
    echo "程序开始执行,请稍等 ..."
    git clone -b Dev git@192.168.1.240:Ivone/$1
    echo "正在创建nginx vhost文件 ..."
    cd /usr/local/nginx/conf/vhost
    fileMsg="server {
	listen 80;
	server_name  $1.com www.$1.com;
	index index.html index.htm index.php;
	root /home/website/$1;
        location ~ .*\.(php|php5)?$
	{
		fastcgi_pass  127.0.0.1:9000;
		fastcgi_index index.php;
		include fastcgi.conf;
	}
	if (!-e \$request_filename) {
		rewrite  ^(.*)$  /index.php?s=\$1  last;
		break;
	}
	access_log /var/log/nginx/$1.log;
        }
    "
    echo $fileMsg > $1.conf
    echo "vhosts文件已生成，正在重启nginx"
    /usr/local/nginx/sbin/nginx -s reload
    echo "测试域名为:$1.com www.$1.com"
    echo "程序执行结束"
fi

#echo $1

