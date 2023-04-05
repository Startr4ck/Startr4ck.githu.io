# CSRF  
## 基础   
**cookie**  
cookie分为两种cookie。  
第一种为临时的cookie，过期时间一般是在浏览器这个进程结束。   
第二种分为本地cookie，本地cookie的过期时间一般是在 set-cookie 头部当中进行指定。 
**csrf**  
csrf的分类 大致可以分为get和post两种类型  
get类型的csrf，一般就是在链接当中直接说明要做什么事情 vuln.com/transfer/money/11111   
post类型的csrf，一般是黑客自己的网站，其中内嵌了一些iframe，iframe当中存在一些post参数表格，当你点击的时候就会向发送一些信息 。注意存在前端可能是post类型，但是服务端接受参数的时候并不指定类型即post和get类型都可以进行接受。 


## 攻击   
### 常见的利用的场景  
你已经登录了存在csrf的网站vuln，这个时候黑客给你发送了一些存在问题的链接 。链接当中对应的域名是vuln，则很可能说明vuln存在get类型的csrf。如果对应的域名是 exploit，则很可能说明当你访问exploit的时候会帮你提交请求为post类型csrf。  

你访问了不良网站，不良网站一直在替你去访问这些请求去攻击存在csrf漏洞的网站vuln。  
所以你应该懂了为啥知乎打开外链要提示，为啥不要看不良网站
  
 
详情例子  
[看雪img改头像](https://www.bilibili.com/video/BV1Aa4y1x7Sd?from=search&seid=12112294959522437693)

### 利用前提  
vuln网站存在漏洞   
一般都是由第三方发送 

## 防御  
正如道哥在白帽子讲web安全当中所讲，csrf的本质就是提交的参数都可以被猜测。那么我们是否能够在请求的参数当中增加一些不能被猜到的部分？  
### 第一种思路 阻止不同外域的访问     
**origin header**   
origin字段 标识请求的域名 
**referer header**
referer字段 标识从哪儿来的
![20211027000401](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000401.png)

第一种思路想必大家都有认识到，某些博客网站当中的图片外链失效就是靠着两个字段
但是同源验证有弊端，第一只能防止在第三方网站的请求，本地网站当中如果存在论坛或者展示就不能进行防护 看雪的例子。 
### 第二种思路 提交时必须有一些在本域当中才能获得的信息   

**csrf_token**
1. csrf token请求的时候放dom树里面给客户端 ，设计为 随机字符串和时间错 
2. 请求的时候本地js遍历拿csrf_token，发到请求当中  
3. 服务端验证时间和有效性，分布式存储csrf_token   
现在的常用方法是 encrypted token pattern  类似 jwt 对信息进行加密   
存在弊端 对服务器的消耗   

**双重cookie验证**  
利用了攻击者只能利用我们的token不能拿到我们的token的特点      
1. 前端向后端发起请求取出cookie拼接url  xxx.com/token=user1  
2. 后端看cookie字段和url参数是否相同即可 

存在弊端 同源策略 ，实现 子域名之类的  


**源头 samesitecookie**  
从协议当中设置   
对cookie设置 samesitecookie属性  
```
Set-Cookie: foo=1; Samesite=Strict 
Set-Cookie: bar=2; Samesite=Lax 
Set-Cookie: baz=3
```
点击链接的话  a.com 到 b.com foo则不会进 但 bar和baz会 
a.com到b.com 是post或者异步的话 则bar也不会 
存在弊端 不支持子域   


### 如何进行挖掘  
1. csrftester   
2. 手动挖掘 
报文当中的验证字段改变 referer origin 改了有没有影响
请求当中是否存在token字段sid之类的 



## referer
https://tech.meituan.com/2018/10/11/fe-security-csrf.html 
