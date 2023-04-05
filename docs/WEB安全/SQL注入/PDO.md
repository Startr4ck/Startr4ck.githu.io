# PDO  
编译预处理是很多文章当中所说的防范SQL注入最好的方法了，但是其是否一定是安全的呢？这篇文章会包括以下的几个问题。   
1. 什么是PDO？
2. PDO和ORM的不同？
3. PDO所产生的安全问题 



## PDO的基础
### PDO的定义
用我自己的话来说，PDO就是PHP官方为了统一数据库的操作以及避免SQL注入等安全问题的产生所以构建的一个数据访问框架。所以这里说的PDO一定是专门针对PHP语言。  
官方的话就是如下  
` PHP 数据对象 （PDO） 扩展为PHP访问数据库定义了一个轻量级的一致接口。实现 PDO 接口的每个数据库驱动可以公开具体数据库的特性作为标准扩展功能。 注意利用 PDO 扩展自身并不能实现任何数据库功能；必须使用一个 具体数据库的 PDO 驱动 来访问数据库服务。 ` [来源于php官方文档](https://www.php.net/manual/zh/intro.pdo.php)   
其实现的方式图示可如下  
![20211017190425](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017190425.png)
### PDO实现的方式  
**操作步骤**  
1. 创建对象  
$dsn是一个数据层 $dsn = "{$type}:host={$host},$db_name={$db_name}"
$pdo = new PDO($dsn,$user,$pass);
调用对象方法，对错误异常进行处理  
昨晚上一直插入数据不成功的原因是插入的sql语句在表名当中没有使用进行包裹  
其实实例当中的数据也是没有进行包裹的但是却成功了
2. 查询操作  
$res是返回的结果集 pdo对象的query方法  
fetch 查询单条  
fetchAll 获取所有的记录  
foreach($res as $row)
对展示出来的结果也需要使用函数对结果集进行处理 
fetch函数一条一条
fetchall 函数全部进行展示  
->rowCount() 展示的是结果集的行数  

3. 模型映射&&链式操作  
简单地来说就是申明一个类，其中的数据属性是private属性，和一个内置的get方法 我们要做的就是在pdo属性当中进行设置pdo的访问方法，然后当访问到的时候返回的就是一个对象而不是一个属性了  
![20211017191612](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017191612.png)
4. 预处理  
预处理的主要作用是为了防止sql注入攻击  
原理 将数据和代码进行分割 ，产生sql注入的时间是在编译期间，预处理是在prepare的时候将模板进行编译了，然后再往其中送入参数数据。
先使用pdo的prepare方法  返回一个预处理的对象  
再执行预处理对象的execute方法得到结果，execute当中保存参数  
![20211017191631](https://picsfor.oss-cn-shenzhen.aliyuncs.com/blogs/imgs/20211017191631.png)  
### PDO和ORM之间的区别   
关于编程语言访问数据库，其实还有DAO，这里就按照自己的理解直接说明之间的区别   
-  PDO：代码访问数据库的统一接口，其访问mysql，postgresql 都是用一套代码。  
-  DAO: 和PDO的概念很像，有点像已经将对应的sql代码封装好成函数，每一次调用函数即可，只是做到了方便，但其实DAO当中的sql函数没有处理好一样会存在sql注入的问题。  
- ORM:强调的是一种思想，即将数据库当中的内容对应成为对象的思想，将操作对象的方式来操作数据，有点MVC当中model的概念。  


## PDO的安全问题  
1. 宽字节注入   
2. 预编译设置当中的安全问题    

### PDO对于安全的防护  
#### 转义特殊的字符  
quote()方法,将一段字符串当中的内容进行转义  
#### 预编译
##### 命名参数  
把参数值当成一个字符串整体来进行处理，即使参数值中包含单引号，也会把单引号当成单引号字符  
```
$pdo=new PDO('mysql:host=localhost;dbname=test','root','root');
```
##### 占位符
问号占位符防止注入  
```
$sql="select * from user where username=? and password=?";
```

##### binParam 方式进行绑定参数 

### PDO分为模拟预处理和非模拟预处理 
模拟预处理 PDO::ATTR_EMULATE_PREPARES 默认为true
PDO内部会模拟参数绑定的过程，SQL语句是在最后execute()的时候才发送给数据库执行。 而模拟参数进行绑定的时候如果数据是攻击者恶意构造的字符串就会造成SQL注入的情况发生。  

非模拟预处理 两个阶段 
1、prepare 阶段 将sql语句模板发送到数据库服务器  
2、execute 函数发送占位符参数给数据库服务器 
#### 主要的安全问题来源的设置     
```
? PDO::ATTR_EMULATE_PREPARES //模拟预处理(默认开启)
? PDO::ATTR_ERRMODE //报错(默认关闭)
? PDO::MYSQL_ATTR_MULTI_STATEMENTS //允许多句执行(默认开启)
```  



### 安全问题总结  
1. 模拟预处理模式下(默认开启)会造成 堆叠注入(默认开启)和 报错注入(默认不开) 
2. 模拟预处理模式下(默认开启)，my.ini文件中设置编码为gbk时会造成 宽字节的注入 
3.  PDO::ATTR_ERRMODE 开启的情况下，无论是否模拟，都会造成报错信息的展示  
4. 非模拟预处理模式下 如果没有进行过滤就直接可以执行 
inline query的注入 



PDO注入的方案 

1、宽字节注入 

只要my.ini当中的编码设置为gbk的时候 %80' 都能绕过转义 


### pdo的安全方案 

1. 禁用模拟预处理语句  
$dbh->setAttribute(PDO::ATTR_EMULATE_PREPARES, false); 
它会告诉 PDO 禁用模拟预处理语句，并使用 real parepared statements 。 
这可以确保SQL语句和相应的值在传递到mysql服务器之前是不会被PHP解析的（禁止了所有可能的恶意SQL注入攻击）。

2. 不使用gbk字符进行编码  
3. 关闭堆叠注入和报错显示  

## referer  
[PDO、DAO、ORM之间的区别](https://blog.csdn.net/qiuxuemei915/article/details/106182304)
[PDO 下的注入思路](https://paper.seebug.org/1636/#0x01-pdo)