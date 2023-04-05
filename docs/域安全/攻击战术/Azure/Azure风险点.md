# AZure 风险点   

以下几种安全风险点全部基于Azure 而产生 

## 安全特点  
### PHS 密码哈希同步

既然域用户的账户密码在本地AD和云当中都可以使用，必然需要一种方法进行同步密码。 

一般在企业当中所使用的方法是 PHS    
下面是示意图    
![20211031225731](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031225731.png)
需要注意的是 AD 用户的密码哈希不会通过网络传输而是通过发送密码哈希的哈希  

AD Connect 当中两个账户一个是 MSOL_xxxx  在本地的AD环境当中

一个是 Sync_xxxx 在azure的环境当中。  

这两个账户在各自的环境当中都是高权限   



### 是否使用了Azure域部署 

```
https://login.microsoftonline.com/getuserrealm.srf?login=80303920@sonicsky.onmicrosoft.com&xml=1
```

通过这个页面能够探测到目标是否使用了 Azure域部署  

注意 

即使只要后缀是正确的就可以判断 



### 外围邮箱爆破  

该邮箱地址是否是正确的邮箱地址，那么我们能够利用这个点来对域内的账户进行爆破并且不会产生任何的日志  

具体的接口为 

```
https://login.microsoftonline.com/common/GetCredentialType
```
![20211031225546](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031225546.png)       

Github当中已经存在相应的工具了。    

[o365creeper](https://github.com/LMGsec/o365creeper)

### 密码爆破

爆破的接口是 EWS接口  

```
https://outlook.office365.com/EWS/Exchange.asmx
```

具体的使用方式是 [Mail sniper](https://github.com/dafthack/MailSniper)
但是需要注意的是会产生大量o365的日志  

## 
## 权限  
和之前的渗透测试几乎相同，需要注意的是其中多了一个叫做MSOL的账户，这个账户是高权限账户，之前我们的目标通常是域控，但是在AZure我们的目标是 MSOL账户   
获取MSOL账户的权限依旧可以通过lsass dump进行 

### 错误配置  
AD域当中的错误配置 
https://www.pentestpartners.com/security-blog/azure-ad-attack-of-the-default-config/



## Refer 

非常有用的知识点  

https://www.synacktiv.com/en/publications/azure-ad-introduction-for-red-teamers.html

