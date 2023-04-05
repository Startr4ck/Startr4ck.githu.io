# ElasticSearch  

ElasticSearch存在比较多的风险比如未授权访问和 几年前的RCE  ，影响最为广泛的是 未授权访问。 



## 未授权访问 

### 造成危害

操纵数据库，查看或者修改其中的内容等 



### 如何搜索

首先寻找开启 9200和 9300端口的服务器。 

访问 其页面  看是否存在内容 You Know，for Search

![20211101000808](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000808.png)

访问IP地址加上/_cat 查看是否有返回消息   
![20211101000839](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000839.png)

若都出现，则说明该服务器存在elasticsearch未授权漏洞



### 如何利用

可以直接通过    [ElasticHD](https://github.com/360EntSecGroup-Skylar/ElasticHD)进行连接，管理其中的 ElasticHD内容

查看其中的数据    
![20211101000904](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000904.png)
甚至可以删除其中的索引等内容，对业务造成极大的危害。
![20211101000928](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000928.png)

### 如何修复 

加上认证即可  

http basic auth 

加上防火墙  

防御

https://cloud.tencent.com/developer/article/1624456

