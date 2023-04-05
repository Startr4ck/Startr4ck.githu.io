# kerberos_pre_auth 

当用户向KDC 服务申请TGT的时候，会发送用户的ntlm hash加密的时间戳。KDC解开这段数据并且获得时间戳，时间戳满足条件即返回TGT。这个过程叫做 pre_auth

攻击者可以利用这个环节进行爆破获取大量的信息 。 如果有错误的配置的话可能还会有as_repRoasting 

分为两种情况： 

某个用户关闭了pre_auth的配置 

主要发生的时间阶段是在kerberos进行预认证的时候进行，

AS_REPRoasting 是在错误配置不需要用户提交client hash 就可以获得TGT

说明我们平时说的TGT并不只是tgt而且包括**TGT**和下一阶段所使用的在as_rep当中的 enc_part进行解密得到的**session_key**

另外的密码喷射和用户枚举也是发生在client请求tgt的时候，但是注意用户枚举只有在命中了才会产生日志，所以不会产生很多错误日志 。





## 攻击手法  

### **AS_REPRoasting** 

如果某个用户配置了不要求kerber 预身份认证的话  

![20211101004511](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004511.png)

意味着我们可以不需要进行验证就可以获取没有配置该选项的tgt和 enc_part 

我们可以对enc_part当中的数据进行解密，enc_part 当中为 用户ntlm_hash 加密的session key，所以一旦我们如果能够获取到其中的数据的话就能够离线爆破从而获得用户的ntlm_hash

```
rubeus.exe asreproast 
```

![20211101004501](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004501.png)

得到设置错误设置的 hash ，之后进行爆破即可得到ntlm



在咱们的内网当中并没有找到这样进行错误设置的 

### kerbrute 

**不需要加入域**，不使用ldap协议进行爆破产生 4625的日志

在pre_auth的阶段错误的密码或者用户名会有不同的返回结果 

会产生 

4768  TGT 请求 keberos 身份验证 请求TGT 

4771 两种日志 ，但是这两种日志的不会很明显

速度非常快 

而且不会有任何明显的日志 

1、看域当中存在的用户 

![20211101004442](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004442.png)

这种方法是基于kerberos认证 返回的域用户信息不同所造成的。





2、使用密码喷射
![20211101004422](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004422.png)





### reference

密码喷射以及验证vaild name的原理 

https://www.cnblogs.com/secxue/p/14969961.html

