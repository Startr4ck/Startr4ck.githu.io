# WPAD  
## 基础  
wpad是web代理自动发现协议简称，是让局域网用户的浏览器可以自动发现内网当中的代理服务器所使用。 
需要注意的是 苹果的 Safari浏览器不支持PAC文件的解析。 
顺序是 
1、从DHCP当中去寻找是否获得了代理配置  
2、如果没有结果从 wpad.domain.com 当中进行解析到结果    
3、没有结果，则使用NetBios NBNS LLMNR 进行解析寻求wpad网站    
4、请求wpad服务器当中的 wpad.dat 当中的资源，其中包含的就是代理的设置。   


在一般的内网环境当中 
已经不能使用 3 的因为 补丁 ms16-077  
所以现在一般是冒充dhcpV6的方式进行攻击，即广播DHCPV6的方式进行spoof    





## 缓解WPAD攻击的方法  

1、在DNS服务器上指定wpad服务器的地址 

2、使用组策略禁止所有internet浏览器的自动检测代理设置 



浏览器传输ntlmv2 hash的方式 

 ![20211101001925](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001925.png)



## Referer

[wpad](https://www.1ight.top/%E5%88%A9%E7%94%A8%E4%B8%AD%E9%97%B4%E4%BA%BA%E6%94%BB%E5%87%BB%E8%8E%B7%E5%8F%96net-ntlm-hash/#WPAD_jie_chi)







是否能够使用wpad.dat进行？
![20211101001953](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101001953.png)


wpad当中的 pac文件举例如下 
![20211101002006](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101002006.png)

