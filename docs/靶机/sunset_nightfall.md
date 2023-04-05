# sunset_nightfall  
## 简述  
https://www.vulnhub.com/entry/sunset-nightfall,355/

## 服务发现和信息收集    
### 扫描信息  
```
nmap 192.168.1.*  
nmap -A  -p 1-65535 192.168.1.106  
```      
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200211194612.png)
对192.168.1.106进行端口扫描  
发现开启的端口都是需要进行爆破的端口或者是特殊的服务的端口  
```
smb-H 发现并不存在权限  
```    
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200211200049.png)
尝试通用的漏洞
```
nmap -v -p139,445 --script=smb-vuln-*.nse --script-args=unsafe=1 192.168.1.106 -Pn
```  
好像并不存在什么漏洞  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200211200954.png)   
既然这样多收集一些信息吧  
### 收集用户信息  
```
enum4linux ip 收集smb协议对应的信息  
```   
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200211205120.png)  
收集到了其中的用户名  
### 爆破密码  
进行爆破端口的密码  
```
hydra -l  -matt -P /usr/share/rockyou.txt
```
发现密码  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200211205346.png)  
登录上去  
发现其中的文件没有什么意思，也没发现什么能够继续下去的地方  
***  
我卡主了  
查看别人的提示之后发现是利用ftp上传ssh文件进行免密码登录  
## 权限
[ssh文件登录](https://www.jianshu.com/p/fab3252b3192)

https://wsgzao.github.io/post/ssh/
```
 ssh-keygen -t rsa  本地生成  
```  
上传公钥到服务器上，我们在本地就可以直接进行登录了  
进行提权  
```
find / -perm -u=s -type f 2>/dev/null  
```  
发现find命令有特殊的可以进行执行  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212104042.png)  
记住要进入scripts文件夹才能使用find命令，不然默认的find命令不在这个文件夹当中  
发现存在nightfall的权限，意味着可以进入nightfall 家目录读取和修改文件  
```
./find find -exec whoami \;
```
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212104316.png)  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212104407.png)
**在find当中查看其中的文件**  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212104708.png)  
拿到第一个flag  
这里可操作的还是太少了，下面有两种方法可以变为nightfall  
### 权限转换  
**1.使用同样的ssh上传文件将我们的公钥上传到nightfall目录下**  
 首先还是需要获得一个连续性访问的shell  
 ```
 find . -exec /bin/sh -p \;
 ```  
 其中find找到的行数决定了命令的结果展示的行数  
 直接反弹shell  
直接复制authorized_keys  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212110730.png)  
 直接登录nightfall  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212111238.png)




**2.使用nc 反弹一个shell**  
本以为反弹的shell会是nightfall账户，但是并不是  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212110032.png)  
![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212110052.png)  

### 权限提升  
现在我们的权限是nightfall  
 ```
 sudo -l 查看其中可以执行的命令  
 ```  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212111321.png)  
 恰好可以使用cat命令查看/etc/shadow 文件  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212111643.png)  
 使用john进行爆破  
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212111953.png)
 ![](https://raw.githubusercontent.com/shakeyin1998/picsformd/master/20200212112055.png)  
 ## 总结   
 存在smb协议，枚举smb的用户  
 对ftp进行爆破获得密码
 使用ftp的上传功能上传了ssh公钥  
 matt登录ssh之后使用find命令进行提权 写入ssh公钥到另外一个用户nightfall下  
 登录nightfall之后发现存在可以使用rroot权限执行cat命令  
 使用cat查看密码文件，发现密码之后使用john进行爆破  
 