# NtlmRelayLdap  

## 简述  
在这里演示进行中继到LDAP服务器当中，利用的攻击方式是 
**基于资源的约束委派获取域内大量高权限主机票据**  

在**NtlmRelayCs**当中，我们通过petitpotam的方式使域控发出ntlm请求到我们控制的中继服务器当中，我们中继ntlm请求到域证书服务器当中从而获取了域控的证书最后通过证书换取了域管理员的黄金票据。  

那么既然我们能够中继到证书服务器，那应该也能中继到ldap服务器当中，在这篇文章当中，我们会利用中继到ldap服务器的方式配合 约束性委派拿下大量权限 
## 造成影响  
1、目前能够以普通域账户的身份获得其他域账户对应主机服务的最高权限。

2、能够任意创建计算机账户  
## 原理  
原理当中涉及到很多图片，如下即可    
![20211030182234](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030182234.png)  
## 实践  
### ntlm 中继LDAP 修改信息 

0、创建一个计算机账户，这个账户自身需要知道密码  
1、创建ntlm的中继服务  
2、通过钓鱼或者流量引导的方式让受害者发送请求  
3、4 获得了对应的ntlm认证之后我们将收到的ntlm请求中继到ldap服务器当中更改用户的ms-delegate 权限 

### 基于资源的非约束性委派获取对应目标的票据 
5、通过S4U2proxy协议扩展获取到访问受害者的高权限账户  

### 实践步骤  
#### 0、创建计算机账户  
这一步可以使用PS脚本，我这里为了方便使用的方式是虚拟机加域   

#### 1、创建NTLM的中继服务  
```
sudo python3 ./examples/ntlmrelayx.py -t ldaps://ldap_server --escalate-user=machine_name\$ --user-delegate-access --no-smb-server --no-validate-privs -debug
```  
上述代码的意思是
- -t ldaps://ldap_server 中继到 ldap服务器当中 
- -escalate-user=luck\$  提升luck$的计算机账户权限
- --no-smb-server  不进行打开smb服务中继
- --no-validate-privs 不检验中继用户的权限（*检验权限花费大量的时间*）  
![20211030182616](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030182616.png)  

#### 2、使用Inveigh伪造dhcp6服务器散播wpad.dat   
```
inveigh -SpooferIP 我的ntlm中继服务器IP地址    
```  
![20211030182934](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030182934.png)  
简单描述下，这个工具通过使用dhcp6分配ipv6的地址并且分配代理文件的方式使内网当中的流量经过我们的中继服务器。  

#### 3、4 获得了对应的ntlm认证之后我们将收到的ntlm请求中继到ldap服务器当中更改用户的ms-delegate 权限  
![20211030183058](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030183058.png)  
当流量进行中继的时候可见已经中继好了  
上述图当中的红框已经提示我们的自己创建的计算机账户已经配置好了对于用户主机的委派。 脚本已经自动将受害者的计算机账户的PrincipalsAllowedToDelegateToAccount 的值设置成了我们自己创建的账户$ ，也可由图可示  
![20211030183306](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030183306.png)  


#### 5、通过S4U2proxy协议扩展获取到访问受害者的高权限账户 

当这个数值进行改变之后，我们就能 通过S4U2proxy协议扩展获取权限了。  
下面实际操作  
```
.\Rubeus.exe s4u /user:luc计算机账户$ /impersonateuser:Administrator /msdsspn:"host/victim.xxx.com" /ptt /rc4:我们自己创建计算机账户$的hash  
```
意思是通过 s4u的扩展协议使用luck$的计算机账户模拟Administrator的权限(*因为域当中Administrator是域管理员*)进行申请受害者的服务票据   
 
#### 6、最后我们得到了票据  
![20211030183516](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030183516.png)   
![20211030183546](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030183546.png)  

#### 7、任意创建计算机账户 

等待中继的时候更换为   
```
python3 ./examples/ntlmrelayx.py -t ldaps://xxx --add-computer  --no-validate-priv  
```   
![20211030183736](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030183736.png)  

### 防御和检测  
回顾攻击流程，我们有如下关键操作   
#### 1、创建计算机账户  
**防御**
设置域账户最多创建的机器账户数量   
```
ms-DS-MachineAccountQuota
```  
对该属性设置为比较小的数值，如果不必要请设置为0，该属性默认的数值为10  
![20211030184223](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030184223.png)  
#### 2、接管ipv6流量  
**防御**
1. 如果内网当中不需要使用 ipv6的话直接防火墙屏蔽所有DHCPV6的流量传入 
2. 如果不需要wpad.dat 的话可以通过组策略进禁用   

```
[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Wpad] "WpadOverride"=dword:00000001
```  
![20211030184323](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030184323.png)   

#### 3、对受害者账户设置委派   
**防御**
ldap相关
1、通过启用LDAP签名和LDAP通道绑定来缓解针对LDAP和LDAPS的中继。
2、将Administrative用户添加到Protected Users组或将其标记为帐户敏感且无法委派来减少攻击面  
**检测**

发现哪些基于资源的约束性委派  
```
Get-ADComputer -Filter {msDS-allowedtoactOnbehalfofotheridentity -like "*"} | Out-GridView
```  
![20211030184527](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030184527.png)
当计算机账户请求访问受害者主机的服务票据的时候一般为高权限账户，在域控当中的日志当中会体现出，可以在日志审计当中添加对于异常请求票据的检测。

## Refer  
[实践的操作](https://chryzsh.github.io/relaying-delegation/)
[域内本地提权-烂番茄](https://mp.weixin.qq.com/s?__biz=MzI2NDk0MTM5MQ==&mid=2247483689&idx=1&sn=1d83538cebbe2197c44b9e5cc9a7997f&chksm=eaa5bb09ddd2321fc6bc838bc5e996add511eb7875faec2a7fde133c13a5f0107e699d47840c&scene=126&sessionid=1584603915&key=cf63f0cc499df801cce7995aeda59fae16a26f18d48f6a138cf60f02d27a89b7cfe0eab764ee36c6208343e0c235450a6bd202bf7520f6368cf361466baf9785a1bcb8f1965ac9359581d1eee9c6c1b6&ascene=1&uin=NTgyNDEzOTc%3D&devicetype=Windows+10&version=62080079&lang=zh_CN&exportkey=A8KlWjR%2F8GBWKaJZTJ2e5Fg%3D&pass_ticket=B2fG6ICJb5vVp1dbPCh3AOMIfoBgH2TXNSxmnLYPig8%3D)

[实战ntlmrelay](https://mp.weixin.qq.com/s?__biz=MzUzNTEyMTE0Mw==&mid=2247484454&idx=1&sn=bedd0331a3e7cfe561d13c72d301d477)

[利用资源约束委派进行的提权攻击分析](https://cloud.tencent.com/developer/article/1552171)

[wagging the dog](https://shenaniganslabs.io/2019/01/28/Wagging-the-Dog.html)

