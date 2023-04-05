# Adidns 
## 简述 
ADIDNS 的全称是 Active Directory Intergrated DNS   中文的意思是 Active Directory集成DNS   
## 基础  
顾名思义就是AD域当中的解析记录，在域当中进行域名解析才会用到的东西，也十分的重要    
查看一下adidns记录的空间   
![20211031215009](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031215009.png)  

## 利用  
### Adidns dump   
利用工具将AD域当中的adidns记录进行dump出来  
![20211031214426](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211031214426.png)


### Adidns 添加记录 

使用LDAP的方式进行添加DNS记录到ADIDNS 区域 
简而言之，就是使用这个方式进行添加DNS记录，当访问一些不存在的域名的时候进行解析到我们想要进行解析的IP上  
**并且主要由于ADIDNS区域DACL允许普通的用户默认创建子对象，所以攻击者可以利用其进行劫持流量**  
举个例子 wsus.xxx.com，当我们在内网的时候，如果该地址没有被注册，我们可以注册wsus，等待中间人攻击。  

## refer   
[Adidns dump](https://github.com/dirkjanm/adidnsdump.git)  
[Adidns Spoof](https://www.thehacker.recipes/ad/movement/mitm-and-coerced-authentications/adidns-spoofing)  
