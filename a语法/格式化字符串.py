name='芙蓉国'
age=18
score=98.5
print('姓名：%s,年龄：%d,成绩：%.1f' % (name,age,score))#%.1f是保留一位小数
print(f"姓名：{name},年龄:{age},成绩：{score}")
print("姓名：{0},年龄:{1},成绩：{2}".format(name,age,score))


s1='bigyunmountn'
s2='specific'
s3='conceivable'
print('{0:*^30}\n{1:*<20}\n{2:*>40}'.format(s1,s2,s3))


#千位分隔符
print('{0:,}'.format(987654321))
print('{0:,}'.format(987654321.123456789))
print('{0:.2f}'.format(987654321.123456789))#后面是字符串则{num:.num}指输出的字符串长度

a=425
print('二进制:{0:b}''十进制:{0:d}''八进制:{0:o}''十六进制:{0:x}''十六进制:{0:X}'.format(a))

"""
2.1 数字格式化
整数

print("{:d}".format(42))       # 42
print("{:05d}".format(42))     # 00042（补零）
浮点数

print("{:.2f}".format(3.14159))  # 3.14（保留两位小数）
print("{:.2%}".format(0.85))     # 85.00%（百分比）
print("{:e}".format(123456))     # 1.234560e+05（科学计数法）
对齐与填充

print("{:<10}".format("left"))   # 'left      '（左对齐，总宽10）
print("{:>10}".format("right"))  # '     right'（右对齐）
print("{:^10}".format("center")) # '  center  '（居中）
print("{:*^10}".format("hi"))    # '****hi****'（用*填充）
2.2 千位分隔符

print("{:,}".format(1234567))     # 1,234,567
print("{:_}".format(1234567))     # 1_234_567（Python 3.6+）
2.3 进制转换

print("{:b}".format(10))   # 1010（二进制）
print("{:o}".format(10))   # 12（八进制）
print("{:x}".format(10))   # a（十六进制小写）
print("{:X}".format(10))   # A（十六进制大写）
3. 嵌套格式化（动态宽度/精度）

width = 10
precision = 3
value = 12.3456789
print("{:{width}.{precision}f}".format(value, width=width, precision=precision))
# 输出: '    12.346'（总宽10，保留3位小数）
或者使用位置参数：

print("{0:{1}.{2}f}".format(value, 10, 3))
4. 对象属性和索引访问
4.1 访问对象属性

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Charlie", 28)
print("Name: {p.name}, Age: {p.age}".format(p=p))
4.2 访问列表/字典元素

data = {"name": "Diana", "scores": [90, 85, 95]}
print("Name: {d[name]}, First score: {d[scores][0]}".format(d=data))
5. 转义大括号
如果要输出字面量 { 或 }，用双大括号：

print("{{Hello}}".format())  # 输出: {Hello}
"""