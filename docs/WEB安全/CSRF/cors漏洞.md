# CORS 配置不当  
这种类型的漏洞说实话没有多大的用处，但是在审SRC的时候经常会发现外部的白帽子喜欢提这个漏洞   
## 基础   
### 什么是cors标准
通过设置http头部字段，让客户端有资格跨域访问资源  
解决浏览器同源策略的不变  

### 什么是cors配置不当
有些服务器响应头当中配置 ACAO为* 
即不管哪种origin头进行请求,ACAO当中都会返回响应的origin数据  

公有资源:Access-Control-Allow-Origin:*  
授权信息:Access-Control-Allow-Credentials: true 同时 Access-Control-Allow-Origin:不为*  
### 危害
某网站a存在cors配置错误，其用户如果点击了攻击者的页面 b则会将用户在网站a的信息给攻击者。

## 利用  
![20211027000633](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000633.png)
![20211027000642](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000642.png)

## 如何防御 
白名单  
不要设置 
Access-Control-Allow-Credentials为True
## 挖掘  
bp扫描自动给你挖     
