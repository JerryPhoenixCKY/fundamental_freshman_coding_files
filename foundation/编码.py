s="我都觉得不对"
s2=s.encode(errors='replace')
print(s2)
print(type(s))
print(type(s2))

s3 = "耶✌"
s4=s3.encode(encoding='gbk',errors='strict')
print(s4)   #✌️会出现错误在strict（报错）    #有replace ignore strict
print(bytes.decode(s2,"utf-8"))

