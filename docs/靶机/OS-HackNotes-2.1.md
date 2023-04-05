# OS-HackNotes  
## 信息收集  
首先找到一个**LFI文件泄露** 
![20211016164936](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164936.png)
爆破其中的密码   
## 初始的权限  
**john 破解**  
```
john pass1 --wordlist=/usr/share/wordlists/rockyou.txt
john --show pass1 #显示破解之后的数据记住不要带字典 
```
tips hydra爆破会使得  

## 越权  

### 逃离rbash   
尝试使用export 进行绕过但是没有办法  
![20211016164950](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164950.png)
还是使用vim 进行绕过 虽然看到的$SHELL 还是rbash但是实质上已经绕过rbash了。
![20211016164959](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164959.png) 
继续john爆破其中的md5   
![20211016165009](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016165009.png)
?:!%hack41  
得到了其中的passwd  猜测应该和 网站的所有者www-data有关系  
尝试登陆其他的用户发现不行  
是否是wp 的admin当中的密码呢？也不是
**这里有个坑**    
他妈的 john进行爆破之后就会存在 ?: 所以真正的密码是  
!%hack41
**查找特殊的命令**  
sudo -l 
那么直接  
```
sudo su 
```
![20211016165020](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016165020.png)
