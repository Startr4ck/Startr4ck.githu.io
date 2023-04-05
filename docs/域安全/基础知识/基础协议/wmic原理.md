# wmic

启动wmic服务

```
service.msc

```
端口果然是135 
和这个服务有关系 
![20211101002246](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002246.png)


```
sc config wmiApSrv start= auto 按enter
```

![20211101002303](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002303.png)

pth的方式 
https://www.ired.team/offensive-security/code-execution/application-whitelisting-bypass-with-wmic-and-xsl


提一个问题 wmic在445禁用的情况是否能用  
当然不能，！！！！！
原理等会再说 先说说实践   
新建一个端口的设置   
![20211101002319](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002319.png)
大致意思是445端口的封闭  
wmic 当中的
![20211101002334](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002334.png)

如果关闭了445端口  

![20211101002352](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002352.png)

![20211101002407](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002407.png)

重新开启 继续可以访问   

原理如下 
https://www.secpulse.com/archives/149206.html
![20211101002421](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002421.png)

## refer  
原理上的东西  

https://www.bbsmax.com/A/GBJrQMNaz0/  

https://www.ired.team/offensive-security/code-execution/application-whitelisting-bypass-with-wmic-and-xsl

渗透测试 

https://blog.csdn.net/wwl012345/article/details/96965447







wmic 的一个使用方式

```
https://www.ired.team/offensive-security/code-execution/application-whitelisting-bypass-with-wmic-and-xsl
```

