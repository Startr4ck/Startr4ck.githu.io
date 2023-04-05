## wsus

如果在自动更新当中存在一个http的网站，进行更新会造成什么样子的后果？  

回忆之前的文章，因为证书服务器没有使用https被中继攻击，其实也是充分说明了内网当中使用http是没有任何安全性可说的。 

wsus是windows update的 服务。客户端会通过wsus获得来自微软的补丁。在内网当中wsus很可能是使用http的方式进行通信

内网环境当中  

![image-20211008110314554](D:\Users\80303920\Pictures\typora图床\image-20211008110314554.png)

## 攻击分析  

可以看到windows注册表当中已经说明了客户端wsus应该寻找什么样的地址选择进行更新 

0、内网原来做了arp的防护那没事了。。。。



1、我们需要让受害者主机解析wsus.xx.com为我们的IP地址

达成这个目的，我们可以使用如下几种攻击向量 

- WPAD.dat 进行
- DNS欺骗 



网络上的向量1 

pywsus  进行伪装 wsus服务器 

bettercap 进行伪装dns 进行欺骗 ，这个要求你受害者以及伪装的服务器在一个子网当中比较难达成 

但是在Hacker Recipe当中实现了 segment2 的实现方式 

https://www.thehacker.recipes/ad-ds/movement/mitm-and-coerced-authentications/arp-poisoning



我们能否使用wpad.dat 进行？ 
考虑使用工具Inveigh, 但是其实这个工具在SpooferIP的情况是广播的PAC是direct的，Inveigh主要是为了进行请求验证的原因  



## Referer 

[即使使用了https也会造成的问题](https://www.contextis.com/en/blog/securing-against-wsus-attacks)  

[对应的使用文章](https://www.gosecure.net/blog/2020/09/08/wsus-attacks-part-2-cve-2020-1013-a-windows-10-local-privilege-escalation-1-day/)

