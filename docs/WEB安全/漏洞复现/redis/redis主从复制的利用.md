# REDIS主从复制提权 
利用第三方库进行提权 ，影响的版本是redis 4.x   
## 原理  
![20211026214804](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026214804.png)  
简单概括下，成为master加载第三方库主从复制中的sync执行过程，设置我们的vps作为从服务器，然后执行命令之后，直接连到靶机上执行第三方模块中的命令结果    
## 实践操作  
本次要进行复现的漏洞就是使用第二种进行  
### 利用前提 
1.我们有一台vps其中开启了redis服务  
2.靶机支持主从服务，也是未授权 版本在5左右，支持第三方模块  
### 实践的结果  
![20211026215002](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026215002.png)

## refer  
[Redis 基于主从复制的 RCE 利用方式](https://paper.seebug.org/975/)

[redis 4.x RCE](https://www.k0rz3n.com/2019/07/29/%E5%AF%B9%E4%B8%80%E6%AC%A1%20redis%20%E6%9C%AA%E6%8E%88%E6%9D%83%E5%86%99%E5%85%A5%E6%94%BB%E5%87%BB%E7%9A%84%E5%88%86%E6%9E%90%E4%BB%A5%E5%8F%8A%20redis%204.x%20RCE%20%E5%AD%A6%E4%B9%A0/)