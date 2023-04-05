# NtlmRelayEws   

## 简述

在前两篇文章当中，我们通过钓鱼和petitpotam以及IPV6流量欺骗的方式，中继机器或者是域用户的账户到了ADcs服务器以及LDAP服务器。

那么除此之外， 我们是可以使用ntlm_relay中继其他的服务器？ 

答案是肯定的，既然我们能够中继到证书服务器，那应该也能中继到Exchange服务器当中，在这篇文章当中，我们会利用中继到Exchange服务器的EWS接口获取大量内网的邮箱的权限 
EWS接口在内网部署了 Exchange的服务器当中都是普遍存在的，我们可以通过这个接口进行获取数据。


## 造成影响 

1、能够获取同网段内或者被钓鱼的员工的邮箱所有权限（可查看邮件内容，发送邮件等）


## 攻击实践
![20211030190712](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030190712.png)

### 1、创建ntlm的中继服务

```
./exchangeRelayx.py -t https://exchange_server/EWS/exchange.asmx -l 10.55.161.252
```

### 2、3 触发和受害者发送ntlm认证  

这里通过钓鱼和IPV6的网络欺骗都可以做，因为不认识有邮箱权限的外部顾问员工，所以直接使用网络欺骗。 
![20211030190748](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030190748.png)

### 4、5 中继到exchange的EWS接口并返回邮件内容  

这两步其实exchangeRelayx 已经集成帮我们做好了,当有受害者的ntlm relay到我们的中继服务器的时候，我们就可以直接操作邮箱了。

![20211030190946](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030190946.png)

最后实现的效果如下 

![20211030190840](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030190840.png)

## 四、检测防御

#### 1、Ntlm Relay 到EWS接口

**防御**

1、如果在实际场景当中不需要ews接口功能的话，可以关闭这个接口

2、不允许ntlm认证访问EWS接口





#### 2、接管ipv6流量

**防御**

1、如果内网当中不需要使用 ipv6的话直接防火墙屏蔽所有DHCPV6的流量传入 

2、如果不需要wpad.dat 的话可以通过组策略进禁用

```
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Wpad] "WpadOverride"=dword:00000001
```
![20211030190859](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030190859.png)

 **检测**

使用流量监测的设备，对内网异常的IPV6流量进行发现和检测 

