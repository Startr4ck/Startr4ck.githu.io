# Azure  基础
Azure AD 并不是部署在云里面的AD 
Azure AD的大致部署图为   
![20211031230201](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031230201.png)
从部署应用图当中就可见     
Azure AD是一种云上的验证资料库类似于部署在外网的sso，连接云当中的应用和外围的其他应用，其AD的部分还是在本地进行部署，**和传统部署不同的是AD当中的公司用户账户信息能够登录其他的云应用。**  
![20211031230211](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031230211.png)


## 密码验证 
windwos 7  和 windwos server 2008 之后支持对加入Azure AD计算机进行身份验证，比如使用 Azure AD 环境当中的 NEGOEX PKU2U  
NEGOEX PKU2U是基于 Kerberos PKINIT消息 即证书请求验证身份。  
所以判断一个服务器是 Azure之后，查看证书是必不可少的  
``` 
certmgr.msc 
```

但是需要注意的是Azure AD 环境和本地的AD环境有巨大的区别，不再基于Kerberos和 NTLM   



## referer

[Azure AD渗透测试](https://www.synacktiv.com/en/publications/azure-ad-introduction-for-red-teamers.html)   
[关于azure的 渗透测试备忘录](https://pentestbook.six2dez.com/enumeration/cloud/azure#traditional-ad-azure-ad-comparision)



