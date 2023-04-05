# insplainsight  
## 简述
https://www.vulnhub.com/entry/in-plain-sight-101,400/  
### 服务发现  
**IP查找**
```
nmap -PR 192.168.1.*
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207143848.png)  
**查找端口**
```
nmap -A -p 1-65535 192.168.1.62
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207144112.png)  
发现端口当中打开了ftp，尝试去发现其中的东西  
注意其中存在一个匿名登录  
查看其中的文件的提示   
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207144409.png)  
提示网站可能使用wordpress，另外在提升权限上和joe有关系，另外可能存在后门文件
匿名登录之后发现权限很少  
以下步骤同时做 
1.尝试爆破ftp的密码   
```
hydra -l ftp -P top6000.txt ftp://192.168.1.61
```
2.继续收集信息  
看看webapp下面的信息  
```
python3 dirsearch.py -e php -u http://192.168.1.62
```  
发现phpinfo文件  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207145710.png)  
发现wordpress文件夹  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207150303.png)
那么直接使用wpscan对该站点进行扫描吧   
```
wpscan --url http://192.168.1.57/wordpress/ --api-token xxxx -e vp 
wpscan --url http://192.168.1.57/wordpress/ --api-token xxxx -e u
```  
查找插件出来都是几个不是很重要的xss漏洞不好进行利用
发现用户名存在bossperson 
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207151353.png)  
对密码进行破解  
```
 wpscan --url http://192.168.1.62/wordpress/ --api-token x -U bossperson -P ../fuzzDicts/passwordDict/top6000.txt 
```
爆破没有爆破出来，出去看别人怎么做的，原来自己输在了收集信息  
当时并没有注意到这个信息  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153020.png)  
打开那个页面  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153116.png)
点击之后出现一个文件上传的页面  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153147.png)  
是否是存在一个文件上传获取shell呢？   
保留观点，打开f12注意其中的数据  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153337.png)
使用base64进行解码  
```
echo c28tZGV2LXdvcmRwcmVzcw== | base64 -d  
```
给出提示
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153544.png)  
翻译过来的意思就是  正在开发的意思？  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207153643.png)    

正在此时 发现爆破bossperson出现了结果  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207155843.png)
 
 对so-dev-wordpress 页面进行扫描也得到了用户名和密码  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207160134.png)  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207160514.png)  
 
 ## 获取权限  
 有wordpress的用户名和密码能够获取wordpress的权限  
 方法有两种，一种是通过写入shell到wordpress页面当中，这种方法要求我们获得的用户名要有更改网站的权限，另外一种是要求我们的用户名是admin才行，直接使用msf当中的方法进行上传文件包获得权限  
 第一种方法：   
 apperance->Theme Editor ->404.Template 编辑其中的php文件  
 
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208023321.png)
 注意要访问特定的404页面而不是随意访问  
 ```
 http://inplainsight/so-dev-wordpress/wp-content/themes/twentytwenty/404.php
 ```
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208023936.png)  
 发现curl也可以进行使用  
 第二种方法：  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207162932.png)  
 发现bossperson的并不能登录 那么使用admin吧  
 顺利反弹一个shell  
 **获取一个普通权限**
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207163046.png)  
 **提权**  
 ```
 python3 -c 'import pty; pty.spawn("/bin/bash")'
 ```  
 获取交互式的shell  
 寻找特殊的权限  
 ```
find / -perm -u=s -type f 2>/dev/null 
 ```  

 **搜寻信息**  
 有一个服务器权限之后，尝试寻找提权你的指令，如果是服务器的话尝试去查找其中的配置文件
 5x:Fxx%x+D#xaCfv  
 从/var/www/wordpress/wp-config.php 文件当中去寻找文件
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207173214.png)  
 没了线索。。。  
 想起有另外一个wordpress 
打开so-dev-wordpress，查看其中的配置文件  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207173937.png)  
oZ2R3c2x7dLL6#hJ  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207174150.png)  
选择好sodevwp当中的sodevwp_users表，其中的Mike很可能和一开始说的那个人是一个人
用户名和密码进行破解  
```
本地破解 john  
john pass -wordlist=/usr/share/wordlists/rockyou.txt
```  
将密码保存到文件当中然后进行上传  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207174851.png)  
得到密码文件之后进行登录  
**变为mike**  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207182233.png)
发现使用ssh不能进行破解，只能su到用户权限  
查看用户的密码文件  
```
cat /etc/shadow  
cat /etc/passwd
```  
提示使用连字符  
```
cat /etc/passwd-  
```  
查看文件内容  
发现密码  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207181513.png)  
**变为joe**  
寻找特殊的权限  
```
find / -perm -u=s -type f 2>/dev/null 
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207181735.png)  
执行文件bwrap  
拿到权限
**变为root**
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200207181829.png)
## 总结  
使用提示页面（类似ctf一般的脑洞）提示有另外一个wordpress站点  
进入站点之后，使用翻看数据库配置的方式获取·数据库密码  
拿到数据库密码之后解密处mike的密码  
得到mike的密码之后查看/etc/passwd-当中的文件得到joe的密码  
在joe的账户当中找到一个特殊的权限指令，使用该指令进行提权  
