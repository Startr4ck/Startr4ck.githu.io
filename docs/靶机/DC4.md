# DC4  
## 简述
使用弱密码进入网页当中，发现命令执行的漏洞，反弹shell 翻其中的数据切换用户 使用命令将新建的用户信息写入/etc/passwd 文件  

## 发现和寻找漏洞 
如何进入网页  
使用burpsuite进行爆破  
```
字典  /usr/share/wordlists/rockyou.txt(bp打开直接卡死)  
字典 /usr/share/john/password.lst  
```

注意在破解的时注意查看其中的用户登录页面，在这个靶机上写了admin登录就不需要使用爆破用户名了  
![20191129154556.png](https://i.loli.net/2019/11/29/IbADzQHscxat5pm.png)  
直接使用burpsuite进行爆破了  或者可以使用Hydra进行爆破(爆破的工具选择)  
![20191129154731.png](https://i.loli.net/2019/11/29/cxmwdD8o1lQaNJy.png)
### WEB漏洞  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201163827.png)
其中存在web的命令执行漏洞，直接bp抓包改包  
![20191129155022.png](https://i.loli.net/2019/11/29/ogYFkiqBwZ3hzOv.png)
得到shell  

![20191129155053.png](https://i.loli.net/2019/11/29/yP5orOCk2nW3sVg.png) 



##  寻找信息  
在/var/mail 当中的右键存储了密码  
在本地备份当中存储了之前的密码  
![20191129155243.png](https://i.loli.net/2019/11/29/Mgi3B9RaJclXdvV.png)  
拿到一个权限之后首先要做的事情就是寻找有用的信息 
现在得到一个密码本使用hydra进行破解  
``` 
hydra -l  jim -P 密码本 ssh@ip 
```   


得到其中的密码  
![20191129155809.png](https://i.loli.net/2019/11/29/ZzFQsMg2LjJKUqt.png)


### 提权   
```
find / -perm -u=s -type f 2>/dev/null  
```
![20191129160117.png](https://i.loli.net/2019/11/29/JYOw46HK2oZUDb7.png)
其中的数据可以看到这个sh脚本有执行的权限，正好看看是否能够对该脚本进行变化  

![20191129160422.png](https://i.loli.net/2019/11/29/YvqeDoE5Z7VucHw.png)
正好权限也挺足的，直接往其中添加/etc/passwd 的内容或者是直接/bin/sh 都是可以的  
**是否能直接拿到权限？** 

拿到jim权限之后
**继续收集信息**  
![20191129161559.png](https://i.loli.net/2019/11/29/YvIUzma6WfwCPy7.png)
直接拿到charles的密码 直接使用密码进行登录  
sudo -l 查看密码  
![20191129161809.png](https://i.loli.net/2019/11/29/NjV6wsaZGgl4iAR.png)
其中发现可以不用sudo使用teehee这个命令  
teehee 就相当于把缓冲区当中的数据写入到文件当中，利用这个特性新建一个用户写入我们的用户再进行登录就可以完成了  

**root提权方式**  
写入用户登录信息在/etc/passwd 当中的文件
但是这个文件一般是必须会用su权限的，这个时候时候使用sudo-l 查看的登录不需要密码的s命令就行了  
 echo "hack::0:0:::/bin/bash" >>/etc/passwd
  
重写的时候发现有问题就直接这样来吧  
```
创建有用户名和密码的用户进入passwd文件 
echo 'pavan:$1$pavan$qv9M3fBmtDPrOTBZflNl81:0:0::/root:/bin/bash' >> /tmp/raj
sudo test /tmp/raj /etc/passwd
su pavan  
对应的密码是123456  
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201164655.png)
## 总结  
简单的弱密码加上命令执行漏洞  
服务器当中存在信息获取两个用户的密码  
最后使用带有su权限的命令往/etc/passwd 当中加入用户  
### 操作  
提权  find / -perm -u=s -type f 2>/dev/null 
### 疑问  
爆破当中如果存在验证码应该怎么办？  
为什么无密码之前行后面又不行了？







