1、waf的类型 

2、waf的原理 

3、如何绕过waf

https://www.freebuf.com/articles/web/226000.html

sql注入waf的绕过方式 

https://www.freebuf.com/vuls/251028.html

## waf原理 

waf的全名为 web 防火墙，就是保护web应用的。 

https://www.freebuf.com/articles/web/224473.html

从 文件传输和错误的输入输出过滤进行 

基本方式是获取用户到服务侧的流量，方式主要有三种。

1、反向代理，读数据进行净化和阻拦部署在服务器之前 nginx openresty都是实现方式。

2、硬件waf，部署位置和反向代理类似，但是获取的是网络层的流量解析为http的流量之后传输给之后的服务器。 

3、网卡流量，读取网卡中的流量并交给服务器数据。

4、混合云waf，cloudflare 

5、软件waf 安全狗       

**原理分类**

基于特征

基于行为 

​                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

绕过waf的思路 

**使用不常规的字符**

sql注入 https://www.freebuf.com/vuls/251028.html

内联注释 

重写关键字 

大小写混写关键字 

编码 十六进制编码 url编码  





**使用不常规的方式**

上传一个webshell，很有可能被杀，但是如果上传一个下载其他webshell的文件被杀的概率就很小。 

上传一个包含的php jsp 脚本，上传一个文本文件进行包含 



**删除特征**

删除报文当中的某些属性 



waf 基于功能分为特殊字符和文件上传两种方式 

**特殊字符**的方式  

大小写绕过，替换关键字 

空格  注释进行绕过 /**/

内联注释 

```
/*!uncion*/ 
/*!select*/
```

十六进制编码

url编码  

关键字 

注释符绕过  

多参数进行传递报文 ，后面不会进行过滤  openresty 

https://www.freebuf.com/articles/web/247655.html



mysql 注入  

/**/ 替换 空格进行注入 

/!/ 内联注释，中间部分继续执行  

chr 函数变换关键字 

base_convert进行转换  

分块传输 绕waf 

更改charset

https://www.freebuf.com/articles/web/259027.html

### 防御

设置web容器无法解析目录中的文件，即使上传也不会有问题 
