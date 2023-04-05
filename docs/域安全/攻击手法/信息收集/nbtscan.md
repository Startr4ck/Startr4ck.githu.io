# NETBIOS  

顾名思义，BIOS大家都很熟悉的一个名词 基本输入/输出系统



NETBIOS意思就是网络当中的基本输出系统，属于同一套API。 





## 原理 

NETBIOS其实包括的是三种服务  

UDP 137 名称服务 

UDP 138 数据报服务  

TCP 139 会话服务 

网上邻居的工作原理，通过广播的方式在 局域网当中寻找计算

机名和对应的IP地址

我们使用NBTSCAN的时候其实是使用的是名称服务进行搜索对应的服务名和IP地址。

### nbtscan   

**nbtscan的原理源于NBNS协议，其中NBNS协议是基于udp137端口，其本质是一种基于UDP传输的应用层协议**

1、在同个网段当中

所以我们实际当中使用到的端口是扫描对方的udp137 端口，请求其中的名称服务  
![20211101001420](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001420.png)

是首先请求内网当中其他主机的mac地址和IP地址，之后再进行NBNS进行请求其中对应的网络名  

![20211101001450](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001450.png)

之后得到的网络名 

2、不和网卡在同一个网段  

如果目标所指定的段，就不会使用ARP的形式进行获取mac地址 



## 引申 

1、UDP广播是不是不能跨域路由器？ 

那是否意味着 NBTSTAT 只能在一个网段当中进行扫描？ 

是的 ，实验当中发现并不是。。。。。 

NBTSTAT 并不是传统意义的广播协议，而是一种应用层协议，其能够对一个网段当中的内容进行扫描并能知道该网段的网络名称   

2、为什么wireshark能抓取到其他网络设备的流量  







## 使用

nmap 当中 

```
nmap -sU --script nbtstat.nse -p 137 
```

msf扫描  

```
use auxiliary/scanner/netbios/bnname 
```

windows 程序  

```
.\nbtscan-1.0.35.exe 10.8.0.101/24
```



## 隐蔽和有效性 

在内网流量当中 NBNS 流量太多了 ，所以防守方不会在意这个的流量  

有效性方面 

NBNS的前提是目标主机打开了139端口，在实战当中会发现大量的高价值目标都关闭了这个139端口 ，所以无效 

但是用来识别工作组当中的主机是十分有效的   

![20211101001531](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001531.png)


![20211101001554](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001554.png)

实际上还是请求的对方的137端口 即名称服务 



## referer

[nbtstat的实现原理](http://blog.sina.com.cn/s/blog_5544469d010007f2.html)

[nbtscan局域网扫描的原理](https://www.cnblogs.com/dongchi/p/12612386.html)

