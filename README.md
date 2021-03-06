- **author:Ivone**
- **last update:2017-3-31**
- **version:1.0.0.2017331_release**

> **0.1版说明：**
> 提供简单的文件对比功能，并且能将修改的文件抓出，并且生成安装文件。  
> **0.2版说明：**
> 添加的不同的项目的配置文件，针对不同的项目进行不同的操作。在操作之前必须在conf中完善项目的垃圾文件（不可上传到服务器的文件），未配置则会报错。
> **1.0版说明：**
> 添加配置文件中的路径，更换文件比对为文件哈希计算，将绝对路径修改为服务器所在路径。

## 测试机代码部署脚本

目前测试机的内网IP地址为：`192.168.1.250`，子网掩码为`24`。
Web服务器目录为：`/home/website/`
测试机`root`密码：`simpway`。
测试机MySQL账户:`root`，密码:`1234`

在website目录下，有一个shell脚本文件：`depoly.sh`，可以帮助直接部署在git仓库中Dev分支的代码，并且能生成相应的与git仓库名相一致的nginx vhost文件马上生效，测试域名会在程序执行结束之前提示。
自己的新代码自己就可以快速部署，并不需要找运维的人来帮助更新代码。
所有的更新必须提交git后方可部署，不要直接将文件提交测试机。

使用说明：
由于是shell语言写的Linux脚本，那么执行该文件前，需要使用sh命令，完整命令为：

```shell
sh depoly.sh "项目名"
```

如果该项目之前没有部署过，那么会自动部署，且生成vhost文件；如果已经部署，则会重新拉取该仓库Dev分支的最新代码。
由于只能获取git上面的代码，最好将测试机配置文件修改好直接上传，将不必要的文件写好*.gitiginore*文件。
中间可能会有报错，及时察觉及时反馈更新程序。
如果需要手机测试或者要很多人测试，可以通知我设置静态路由，将IP与域名绑定，不需要修改本地host文件即可直接访问。


## 正式服务器提交安装包生成脚本

目录结构：

``` shell
package：
    |__ install(安装包所在目录，都是tar.gz安装包)
    |__ package(安装包文件备份，都是文件夹的形式)
    |__ sync.sh(执行的入口文件)
    |__ compare.py(具体文件对比操作)
    |__ conf (配置文件目录)
        |__ conf.py (所有项目的配置文件，包括忽略的文件、目录、服务器项目路径)
```

正式机提交现在已经简化为将安装包(补丁)交给运维来上传服务器，可以减少双方的工作量，况且可以自动生成有效的安装包，避免了人工上传带来的失误。

使用说明：
在测试机的`/home/script/vlib/`下面，执行命令：

```shell
sh sync.sh "项目名"
```

脚本会自动将上次master版本中代码与本次比较，然后在package下面生成对应项目名称的目录，格式为

> 项目名+时间戳

注意：
在提交代码时，一定将不需要的文件删掉，并写好*.gitiginore*文件!!!

在生成安装包之前，先查看conf/下的该项目配置文件是否有效，更改为最新配置后再生成安装包。
