## ACLS 
一些和提权相关性比较高的acls   

#### AddMembers 

将任意的用户，组或者计算机添加到目标的组当中  

比如某个用户对Domain admins 有写入成员的权限  



#### ServicePrincipalName

写入spn的权限就可以对这个对象进行kerberoasting了

 

#### GPC-File-Sys-Path

配置组策略 



#### User-Force-Change-Password

更改某个用户的密码 

#### Dcsync 

同步域当中的密码 

####  WriteDAC

将新的ace写入目标DACL的功能

即向目标对象的DACL写入新的ACE，从而使攻击者完全控制目标对象 



https://daiker.gitbook.io/windows-protocol/ldap-pian/12#1.-yi-xie-bi-jiao-you-gong-ji-jia-zhi-de-acl-quan-xian-jie-shao

