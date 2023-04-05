# PTH PTK PTT 

PTT 就是最简单的 pass the ticket ，通过传输黄金票据和其中的session_key ，也可以是获取了服务的hash之后自己创建对应的白银票据，其中白银票据其实也包括其中的session_key 

## kb2871997

无法通过本地管理员的权限对远程计算机使用 psExec WMI smbexec schtasks at 等命令。



## PTH 

pass the hash，这里说的hash是 ntlm hash 

1、**kb2871997** 能缓解pth 但是不能杜绝pth，**域管理员和在本地管理员组当中的域用户是可以进行pth的**。其实winrm当中它也是只能使用RID为500的用户和本地管理员当中的域用户登录。实战当中一般是对网段当中的主机进行喷射密码。 

2、禁止NTLM也使得psexec无法利用ntlmhash进行远程连接。 

3、LAPS的出现解决域内的主机的本地管理员密码相同的问题。



这个的关键是在于是否存在UAC的方式



**在windows当中如果是在本地管理员的域账户或者是rid为500的账户**具有高完整性令牌才能进行pth。



[RID 的hijacking](https://xz.aliyun.com/t/2998)





### 问题

1、pth的本质是什么？

2、创建admin$的方式 

3、本地令牌的问题 



## pass the key 

pass the key是在kb2871997之后产生的新的攻击方式

**攻击条件是：受害者的主机必须存在kb2871997补丁**

进行认证的时候生成的hash的类型决定了是pth还是ptk。 

ptk的意思是pass the key ，其中的hash是aes key，可以使用

```
sekurlsa::ekeys 
```

导出aes key。然后使用 ptk进行传递 

```
mimikatz "privilege::debug" "sekurlsa::pth /user /domain /aes "
```



