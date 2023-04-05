# kerberoast

## kerberoast的关键

只要用户有TGT就可以从KDC请求任何一个服务的TGS票据。如果TGS的加密方式是RC4的话就可以进行破解从而获取hash。如果正好是用户的hash的话就能获取用户的ntlmhash 





## 白银票据的关键  

**白银票据成功的前提 有些服务不去验证 PAC的签名** 

所以如果将目标主机配置为验证PAC签名的话，银色票据就会出现错误。这里可以引申 

ms 14 068

~~或者说你已经知道了服务的密码，然后自己创建能够访问该服务的pac~~

因为，pac是只能kdc进行查看和制作，所以白银票据的关键是只有kdc能够制作和查看pac

![20211101004245](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004245.png)

当服务端获得了TGS之后，使用自己的hash进行解密，解密成功之后将pac发送到域控当中，域控进行解密PAC，获得sid等用户的信息判断是否有访问服务的权限，如果有访问权限就允许访问。



rc4 和 白银票据相关的东西 

https://www.4hou.com/posts/6m99

**结论** 

因为有PAC的存在，所以即使获得了服务的hash也不能伪造真正高权限的票据。

你可以使用服务的hash对高权限的账户进行签名，

但是所幸大多数的服务票据不会去验证PAC的签名，所以是可行的。



## 0、基础 

机器账户默认注册spn为本身的host/machine_name ，用户账户默认不进行注册spn。 



### 1、默认的加密票据加密算法是什么？    

#### 计算机账户

请求的 SPN 注册的帐户上，msDS-SupportedEncryptionTypes 字段的值决定了 Kerberoast 流程中返回的服务票证的加密级别。

**这个设置默认设置在机器账户上，如果没有定义或者设置为0则表明是默认是使用RC4对服务票据进行加密。**

![20211101004309](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004309.png)

这里的计算机账户 设置的0x1c 即默认为aes256进行加密 



#### 用户账户 

用户账户上**一般没有进行定义，默认为空**，默认的属性值是0x7，意味我们是可以请求到使用rc4加密的票据的 

如果 msDS-SupportedEncryptionTypes这个属性值设置为24的话

也可以使用 rc4进行请求 ，当然rc4的加密类型是23的





#### 意外的情况 

即使使用了servicePrincipalName字段设置了对用户账户启用了AES，但是还是能够请求到rc4的票据
![20211101004326](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101004326.png)



[默认密码的相关文章](https://www.4hou.com/posts/6m99)

[如何对rc4当中的链接进行更改](https://myotherpcisacloud.com/post/disable-rc4hmac-and-others-in-active-directory)





2、如何指定加密算法的票据? 8.27

3、是否能够自己进行设置 spn 

4、目前比较好的防御和检测的方式是什么？ 

5、rc4

5、kiribi 和 ccache的 方式 



一般默认没有设置服务的密码类型 

但是可以自己进行设置为 aes 128 或者 aes 256 

但是可以自己进行设置为rc4的方式进行请求ticket





### 2、攻击思路 

1、搜索所有支持rc4加密类型的高权限用户注册的项目 

```
Rubeus.exe kerberoast /rc4opsec
```





```
Add-Type -AssemblyName System.IdentityModel  
```

```
setspn.exe -q */* | Select-String '^CN' -Context 0,1 | % { New-Object System. IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $_.Context.PostContext[].Trim() }  
```



