# ShadowCredentials
## 简述  
顾名思义，这个意思是叫做影子凭证，和基础的kerberos当中的凭据类似都可以进行认证使用。  

## 基础  
### 名词解释 PKINIT 
在第一步获得TGT的时候在kerberos当中是通过挑战应答的方式进行的，是使用用户的NTLM HASH进行的。但是其实存在另外一种方法，使用证书去请求TGT，这种方式叫做 PKINIT。
### 过程大致为   
客户端拥有公私钥，解密证书需要公钥，KDC通过证书来判断，并且利用公私钥来交换session_key 	

客户端的公钥被设置在 msDS-KeyCredtialLINK kcl 当中 ，该客户端可以是用户也可以是计算机 



### 攻击的使用条件 
1、域的DC环境必须在 2016之后，因为 2016之后才能使用PKINIT的方式进行  
2、拥有一个能够编辑对象 msD  
3、需要DC有自己的公私秘钥对，只要有AD CS 和 CA服务就行   

CA 是证书颁发机构 
CS 是证书服务 


### 攻击流程  
攻击的大致流程
1、创建 RSA密钥对   
2、创建X509的证书并且使用1的公钥   
3、将msDs-KeyCredentialLink添加到对象当中  
4、使用PKINIT进行验证获得对象的 私钥   





## 注意事项 

用户账户不能编辑自身的 MSDS KCL 属性 但是机器账户可以。

一般是考虑使用机器账户进行中继达成目的，
![20211031220922](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031220922.png)

在这里只有SMBV1和HTTP两种方式能够达成目标，实际环境当中 SMBv1在vista时代已经默认关闭，所以只能靠http触发。
靠http触发有两种方式
1、webdav  
2、webclient


![img](https://mmbiz.qpic.cn/mmbiz_jpg/icqm3vRUymZntHkcU5XRougmqQwvGtslScCU33hfQXHRzOMFzDxDRSnoQhPJBuRmWbclbib2QFaMXvdqvkrzN7AA/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

### 使用方式
因为其利用的向量比较少，需要高权限的账户，更多地可以考虑将其作为一个留后门的方式使用 
1、留后门的方式进行 
中继向量能够进行破坏的方式   

1、在webdav上可以使用 （需要搜索）
2、在 没有安装 2019-1040补丁的服务器上可以使用smb+efs进行攻击 
在这种情况下简直是神器，一个printerbug + 1040 remove mic之后就直接 中继到ldap 进行dcsync 爽歪歪
## 实践操作   
```
python3 ntlmrelayx.py  --shadow-credent --shadow-target 'dc2$' -t ldap://dc4 --remove-mic 

python3 ./examples/ntlmrelayx.py  --shadow-credent --shadow-target 'N80303920$' -t ldap://xxxxx   --no-validate-privs -debug
```

![20211031221009](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031221009.png)

意思是现在我可以通过这个这个证书进行申请TGT了，但是这里显示权限不够 因为是域用户账户的原因 ,只能是机器账户进行申请，

如果有机器账户的原因则需要考虑使用webdav webclient的方式进行请求 

## 检测
### 创建当中  
1、使用PKINIT需要使用修改对象账户的msDS-KeyCredtialLINK 字段  
### 进行验证的时候   
1、域控当中会产生 4768日志，并且 指示证书信息属性不为空时的异常行为，即日志当中的Certificate Information 当中的 Certficate Issuer Name 字段不为空





## 计划 
1、使用工具或者语法去查询哪些对象配置了这个属性  
2、如何进行寻找配置了 webdav的服务器？ 



## Referer

https://www.thehacker.recipes/ad-ds/movement/kerberos/shadow-credentials

https://mp.weixin.qq.com/s?__biz=MzU0MDcyMTMxOQ==&mid=2247484483&idx=1&sn=784f5cde7c4158e1855e09bfeb5eae1d

