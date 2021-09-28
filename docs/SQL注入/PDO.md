1、什么是PDO？

2、PDO和ORM的不同？

3、PDO的原理？

4、PDO注入实战 







### PDO注入实战  

内容主要来源于  

https://paper.seebug.org/1636/#0x01-pdo



pdo的防御方式

1、特殊方法进行转义过滤 

quote进行转义类似于addslashes之类的 



2、预编译进行处理 

**占位符**  

命名参数防止注入

```
$pdo=new PDO('mysql:host=localhost;dbname=test','root','root');
```

问号占位符防止注入  

```
$sql="select * from user where username=? and password=?";
```

binParam 方式进行绑定参数 



**pdo分为模拟预处理和非模拟预处理** 

模拟预处理 PDO::ATTR_EMULATE_PREPARES 默认为true

非模拟预处理 两个阶段 

1、prepare 阶段 将sql语句模板发送到数据库服务器  

2、execute 函数发送占位符参数给数据库服务器 

主要的安全问题 

```
? PDO::ATTR_EMULATE_PREPARES //模拟预处理(默认开启)

? PDO::ATTR_ERRMODE //报错

? PDO::MYSQL_ATTR_MULTI_STATEMENTS //允许多句执行(默认开启)
```



如果没有进行过滤就直接可以执行 

inline query的注入 

模拟预处理(默认开启)会造成 堆叠注入(默认开启)和 报错注入(默认不开) 

是不是只有模拟预处理开启之后才会有多句执行？





PDO注入的方案 

1、宽字节注入 

只要my.ini当中的编码设置为gbk的时候 %80' 都能绕过转义 









pdo的完美方案 

```
$dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); 
它会告诉 PDO 禁用模拟预处理语句，并使用 real parepared statements 。

这可以确保SQL语句和相应的值在传递到mysql服务器之前是不会被PHP解析的（禁止了所有可能的恶意SQL注入攻击）。
```

