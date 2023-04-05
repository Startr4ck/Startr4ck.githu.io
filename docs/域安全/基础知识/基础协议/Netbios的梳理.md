# netbios 
## 综述  
netbios一般是名称解析，但是现在都存在DNS，所以现在的作用类似于planb 可以考虑进行对其中进行禁用   

## NetBios基础定义  
netbios是网络基本输入输出系统，提供了OSI模型当中的会话层服务，让不同的计算机之间传输分享数据，严格来说并不是一种网络协议，**而是一种应用程序的接口** 
![20211026230236](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026230236.png)
按照图片上面说的，其中存在三种服务  

## 禁用  
查看是否是开启的  
```
ipconfig \all  
```
![20211026230246](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026230246.png)
**方式一**
"控制面板"-->"网络连接"-->"本地连接"-->选中本地接连右键单击"属性"，在新的窗口中，依次为选中"internet 协议(TCP/IP)"-->"属性"-->"高级"-->"WINS"，然后选中"禁用 TCP/IP 上的NetBIOS(s)"，然后"确定",如下图:  
![20211026230304](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026230304.png)
**方式二**  
计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NetBT\start 数值设置为0x4  
**方式三**
HKEY_LOCAL_MACHINE \ SYSTEM \ CurrentControlSet \ Services \ NetBT \ Parameters \ Interfaces \ TCPIP_GUID（TCPIP_GUID将是您计算机中唯一的PER适配器）。编辑“ NetbiosOptions”的数据，并将参数设置为2（默认情况下为0）
## 三种功能
### NBNS  
**简述**  
137 NetBios names 负责对netbios名字和ip之间进行相互的解析 类似于dns    
计算机名称到IP地址的管理方式  
**工作的方式**
第一种 位于同一工作组的电脑之间利用广播功能进行计算机名的管理  
电脑在启动或者是联网的时候，会查询在局域网下是否是存在具有相同的NetBios名称的主机  

第二种 利用WINS(Windows 因特网名称服务)管理NetBios名称  
WINS服务器用于记录计算机NetBios名称和IP地址的对应关系，供局域网计算机查询，系统启动的时候会将自己的NetBios名称和IP地址的对应发送给WINS服务器   

第三种类似于DHCP分配IP地址，第二种里面说的WINS服务器就类似于DNS服务器，将NetBios的名称和ip之间相互对应  

**相关的命令**  
```  
NBTSTAT列出来指定名称的名称和IP以及会话表等等  
NBTSTAT -A ip地址  查询该IP所对应的NetBios名称，命令的本质是向该IP地址对应的137端口发送查询的信息    
nbtstat -c 进行查看缓存   
Add name  
Add group name  
Delete name  
Find name

```
如果有多个网卡，则是从第一个网卡开始进行发送  
![20211026230325](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211026230325.png)
### NBDS  
无连接方式  
138 NetBios datagrams NetBIOS环境下的数据包交流 ，一般用于报告错误，信息广播等  
使用138端口广播自己的NetBios名称，收到NetBios广播的计算机追加到浏览列表中  
发送和接受广播或者非广播的数据包  
**工作的方式**  
关闭电脑的时候，计算机通过138端口广播，收到广播的计算机会将计算机从浏览列表中删除  
当计算机开启的时候，也会进行广播，收到请求的主机会将信息写入到计算机列表当中  


### 会话服务  
139 NetBios sessions  NetBios环境下的会话 ，有连接的方式，提供错误检测和恢复  
主要是进行传输两台计算机之间的信息


[wiki-netstat](https://en.wikipedia.org/wiki/NetBIOS)  
[disabled nbtstat](https://10dsecurity.com/saying-goodbye-netbios/)     
## 渗透当中进行利用    
一般netbios在其中的应用都是通过扫描主机，和进行欺骗拿hash的方式 ，配合进行WPAD欺骗  
### 收集信息
#### windows  
```
nbtstat -n 
nbtscan
```   
查看本地的缓存的netbios 表  

#### LINUX  
**nmap进行扫描**  
```
nmap -sU --script nbstat.nse -p137 192.168.1.0/24 -T4
```  
**msf扫描**  
```
msf > use auxiliary/scanner/netbios/nbname
```  
### 获取hash  
明白在获取服务器的地址的时候，一般是先通过host文件，然后是DNS服务器，最后是NBNS获取IP地址  
**msf方法**  
1.欺骗  
auxiliary/spoof/nbns/nbns_response  
2.capture  
use auxiliary/server/capture/http_ntlm   
use auxiliary/server/capture/smb

https://www.freebuf.com/articles/5238.html  

https://www.anquanke.com/post/id/170471
https://www.freebuf.com/articles/web/164515.html
https://www.freebuf.com/articles/network/165392.html
### WPAD
通过NBNS的来广播wpad 其实在 MS16-077 已经失效了  
只能用于极少数没有安装补丁的终端   

## 扩展  
[NBT欺骗Web代理自动发现协议WPAD](https://paper.seebug.org/papers/Archive/drops2/%E5%88%A9%E7%94%A8%20NetBIOS%20%E5%8D%8F%E8%AE%AE%E5%90%8D%E7%A7%B0%E8%A7%A3%E6%9E%90%E5%8F%8A%20WPAD%20%E8%BF%9B%E8%A1%8C%E5%86%85%E7%BD%91%E6%B8%97%E9%80%8F.html)