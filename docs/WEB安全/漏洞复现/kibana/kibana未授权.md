## Kibana

之前说到了ElasticSearch，那么不得不说Kibanna了。一般安装了ElasticSearch就会安装Kibanna对其中的数据进行分析。 





Kibana 默认配置就没有配置鉴权，所以很容易存在未授权访问的漏洞。

Kibana不止有常见的未授权访问漏洞，同时存在RCE漏洞。





### 造成危害


![20211102232649](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211102232649.png)
### 如何寻找

寻找开启 5601端口的服务器  

访问服务器发现不需要进行鉴权 

### 如何修复

鉴权  



### 总结 

