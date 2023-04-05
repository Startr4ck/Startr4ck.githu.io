# PHPMYADMIN 4.8.X LFI TO RCE  
## 分析   
漏洞分为两块，一块是LFI，一块是RCE  
### LFI 
首先说 LFI   LFI的存在原因是因为其中对于参数并没有做很好的过滤  分析LFI的原因  LFI  index.php 当中存在LFI的php文件  
![20211026215343](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026215343.png)  
第一个红色箭头所指的变量我们是可以进行控制的  
前三个判断的要求是  
1.必须是字符串  
2.不能以index进行开头  
3.不能在黑名单当中  
但是最主要的是第四个要求  见下图  
![20211026215416](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026215416.png) 
满足这三个要求的任意一个都可以。  
#### 第一个是在白名单当中   
#### 第二个  
##### mb_strpos   
mb_strpos 是取这个一段字符串当中某个字符的位置  
##### mb_substr  
mb_substr 是从$page当中的第0个位置去取指定长度的字符串  
本来的意思就是从page这个字符串当中去取第一个?之前的字符串 
```
比如$page=’wqdd?cub?’
那么取出来的东西就是wqdd，判断wqdd是否在白名单当中，如果在的话就满足条件
```
那么这里我们可以使用 
```
$page = a.php?../../../etc/passwd 的形式进行  
```
但是这个表达式的语法意味着包含的文件为 a.php?../../../etc/passwd  ，在php程序当中会将?之后的东西当做a.php文件的参数 
#### 第三个和第二个完全一样  
但是加上了decode的方法，我们利用这个方法可以完美绕过之前说的? 的问题    

### 实际传入  
我们传入的$apge = a.php%253f../../../../etc/passwd  
传入到服务器的时候经历一次decode变为 a.php%3f  
然后在判断的时候再经历一次decode变为 a.php?  可以满足条件  
但是实际在包含的时候确是 a.php%3f../../../etc/passwd 也可顺利包含文件  
```
payload  
/index.php?target=db_sql.php%253f/../../../../../../windows/system.iniRCE 
```
### RCE
造成rce的原因是因为可以通过phpmyadmin写数据到文件当中，然后LFI进行包括其中的文件就行了  
#### 写入文件  
1.在phpmyadmin当中写入文件到数据表当中  在mysql当中如果创建表的话，其中的数据会存放到frm文件当中,如下图所示  
![20211026215926](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026215926.png)  
可以看到写入的文件内容放到了 /var/lib/mysql/ 库名的表名当中
如果可以包含该文件的话就可以rce  
那么我们传入的payload为   
```
payload  
/index.php?z=phpinfo();&target=db_sql.php%253f/../../../../../../../../ruanjian/phpstudy/PHPTutorial/MySQL/data/test/abc.frm
```
但是在docker环境当中并不能，因为mysql的环境和phpmyadmin的环境是分开的。  
#### 执行记录  
每一次我们在phpmyadmin当中执行命令都会产生记录  
因此 我们可以执行一条 SELECT '<?php phpinfo();?>'
然后包含/tmp下的sess文件就会执行命令    
![20211026220039](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026220039.png)  
然后进行远程包含这个文件   
![20211026220051](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026220051.png)  

## 总结  
LFI的原因是因为在对参数进行过滤取得的时候可以使用编码等进行绕过,在于对参数的过滤没有到位  
RCE的原因是phpmyadmin存储数据的时候首先会存储到frm文件当中，可以LFI其中的frm文件


## 思考  
为什么第三块会存在decode这个操作，这是十分诡异的，看起来好像没有什么危害。往往是一块一层没有危害，但是两块加在一起就出现想象不到的危害    
所以进行代码审计的时候  
1. 千万要注意用户可以控制输入的变量  
2. 注意很多地方的decode