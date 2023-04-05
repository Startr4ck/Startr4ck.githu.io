# GPP 组策略提权  
## 原理和基础  
### 前提  
得到所有域主机的本地管理员密码KB2962486安装了这个补丁之后无法通过组策略去设置密码 。  
### 漏洞是如何产生的  
本质是因为在之前域管理员对所有的主机设置密码的时候会使用gpp策略，一般都是将文件放在sysvol这个文件夹当中，这个文件夹当中存在一些密码的aes加密，ms也公布了公钥我们可以对保留的密码进行解密得到真实的密码。   
## 配置和实践    
![20211026211803](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026211803.png)  
设置密码  
这个时候出现危险操作提示  
![20211026211832](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026211832.png)  

## 利用   
使用powershell 进行搜索  
或者直接遍历域控的制定目录即可获得  
![20211026211959](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026211959.png)

## 防御  
1、使用LAPS批量管理域内主机本地管理员帐户  
2、域控安装补丁KB29624863、不在组策略中使用域控密码  
3、设置共享文件夹\SYSVOL的访问权限5、使用PsPasswd批量修改域内主机地管理员密码
## refer  
[利用SYSVOL还原组策略中保存的密码](https://3gstudent.github.io/%E5%9F%9F%E6%B8%97%E9%80%8F-%E5%88%A9%E7%94%A8SYSVOL%E8%BF%98%E5%8E%9F%E7%BB%84%E7%AD%96%E7%95%A5%E4%B8%AD%E4%BF%9D%E5%AD%98%E7%9A%84%E5%AF%86%E7%A0%81)