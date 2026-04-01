import pandas as pd
data = {'a':[1,2,3,4,5], 'b':[2,3,4,5,6], "a**b":[1,8,81,1024,15625]}
s1 = pd.DataFrame(data, columns=['a', 'b', 'a**b'])
print(s1)
print(s1.to_string(index=False))


m,n=input("请输入两个值:").split()
#split()让一行可以输入多个值，用空格分开
print(m)
print(n)


#三重引号 '''...''' 可以保留原始格式（多行、缩进、空格）


import turtle
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.done()



x=float(input("输入a的值:"))
y=float(input("输入b的值:"))
z=x+y 
print(z)


print('qwe\nerror\nefff')  #\n为换行符


int('    35   ',8)  #int里的，8表示进制是八进制


i,*j=[1,2,3]    #带星号变量名实现扩展序列赋值
print(i)
print(j)


p=1
q=2
print('%-8dQWERTYU\nASDFG%8dGHJKL'%(p,q))
#“d” in print(‘%d’%v) means the variable v is integer type; 
# “f” in print(‘%f’%v) means the variable v is a floating point number; 
# “s” in print(‘%s’%v) means the variable v is a string. II-Formatted Output-A
# Determine the space for the variable to be shown: 
# the number(‘8’) before ‘d’ in print(‘%8d’%v) means 8 spaces for the integer v;
# the number(‘7.2’) before ‘f’ in print(‘%7.2f’%v) means 7 spaces for the floating point number v while keeping the 2 digits after decimal point ‘.’. 
# To align the result leftward, add the symbol ‘-’: print(‘%-8d’%v) will make the integer v printed from the left of the 8 spaces. Without ‘-’ will align the result rightward.

d=1
e=2
print('d is %d;e is %d;d+e=%d'%(d,e,(d+e)))



#ast.literal_eval(node_or_str)
#eval(expr, {"__builtins__": None}, {"x": 10, "y": 20})



    

mon=int(input('enter a month(1-12):'))
day=int(input('enter a day:'))
daysinmonth=(31,28,31,30,31,30,31,31,30,31,30,31)
if day<daysinmonth[mon-1]:
    print(mon,'/',day)
else:
    mon=mon%12+1
    print(mon,'/',1)    
    
####################################################
i=0    
while i<3:
    username=input('请输入用户名：')    
    pwd=input('请输入密码：')
    if username=='CKY' and pwd=='123456':
        print('登录成功')
        break
    else:
        if i<2:
            print('用户名或密码不正确，你还剩',2-i,'次机会')
    i+=1
else:
    print('三次机会都用完了')

    
##################################################

    for i in range(1,10):
       for j in range(1,i+1):
           print(str(i),'*',str(j),'=',str(i*j),end='\t')
       print()  #用于换行！！！
       
       
#####################################################3
import random

rand = random.randint(1, 100)
count = 1

while count <= 10:
    num_input = input('请输入您要猜的数：')

    # 尝试转换成整数，如果失败就提示重新输入，不消耗次数
    try:
        num = int(num_input)
    except ValueError:
        print('输入错误，请输入一个有效的整数！')
        continue  # 不计次数，重新输入

    # 判断大小
    if num == rand:
        print('答案正确！🎉')
        break
    elif num < rand:
        print('猜的数太小了')
    else:
        print('猜的数太大了')

    count += 1

if count > 10:
    print('只能猜十次，您失败了 😢')
    print(f'正确答案是：{rand}')
    
    
    
###########################################################
name = "小明"
age = 18

# 使用 f-string
print(f"我叫{name}，今年{age}岁。")
# 输出：我叫小明，今年18岁。
#里面的 f 是 Python 中一个非常实用的功能 —— 它叫做 f-string（格式化字符串字面量），是从 Python 3.6 开始引入 的。
# f 的作用：让字符串中直接“嵌入”变量或表达式    

###############################################################
#.strip() 是字符串的一个方法，用于“去掉字符串开头和结尾的空白字符”（比如空格、制表符 \t、换行符 \n 等）。
#.lstrip() —— 只去掉左边空白
#.rstrip() —— 只去掉右边空白
#.strip(chars) —— 可指定要去掉的字符（不只是空白）
#   s = "   hello world   \n"
#print(repr(s))         # 输出：'   hello world   \n'
#print(repr(s.strip())) # 输出：'hello world' 
    
######################################################################    
#repr()返回一个对象的“官方”字符串表示形式 —— 通常是开发者调试用的，力求“无歧义、可重现”。    
#s = "  Hello, World!  \n"
#print(str(s))     # →   Hello, World!  
                  # （你看不到空格和换行）
#print(repr(s))    # → '  Hello, World!  \n'
                  # （你能看到前后空格、换行符 \n、还有引号！）    
    
'''
score = input("请输入分数等级 (A/B/C/D): ").strip().upper()

match score:
    case 'A':
        print("优秀！")
    case 'B':
        print("良好！")
    case 'C':
        print("及格。")
    case 'D':
        print("需努力。")
    case _:  # 默认情况，相当于 else
        print("输入无效！")



command = input("请输入命令 (start/stop/restart/help): ").strip().lower()

match command:
    case 'start' | 'run':
        print("系统启动中...")
    case 'stop' | 'halt':
        print("系统停止中...")
    case 'restart':
        print("系统重启中...")
    case 'help' | '?':
        print("显示帮助信息...")
    case _:
        print("未知命令")
→ 一个 case 可以匹配多个值，用 | 分隔！


匹配数据结构（列表、元组、字典等
point = (1, 0)

match point:
    case (0, 0):
        print("原点")
    case (0, y):
        print(f"Y轴上，y={y}")
    case (x, 0):
        print(f"X轴上，x={x}")
    case (x, y):
        print(f"普通点 ({x}, {y})")
    case _:
        print("不是有效坐标")


response = (200, "OK")

match response:
    case (200, msg):
        print(f"成功：{msg}")
    case (404, msg):
        print(f"未找到：{msg}")
    case (500, msg):
        print(f"服务器错误：{msg}")
    case (code, msg):
        print(f"其他状态 {code}: {msg}")
        
user = {"name": "Alice", "age": 25, "city": "Beijing"}

match user:
    case {"name": name, "age": age}:
        print(f"用户 {name}，年龄 {age}")
    case {"name": name}:
        print(f"只知道名字：{name}")
    case _:
        print("未知格式")
        

num = 15

match num:
    case x if x < 0:
        print("负数")
    case x if x == 0:
        print("零")
    case x if x <= 10:
        print("1到10之间")
    case x if x <= 20:
        print("11到20之间")  # ← 这个会匹配
    case _:
        print("大于20")
        
   
捕获变量 + 解构赋值
data = ["error", "File not found", 404]

match data:
    case ["success", result, code]:
        print(f"成功，结果：{result}，状态码：{code}")
    case ["error", message, code]:
        print(f"错误：{message} (状态码 {code})")  # ← 匹配这个
    case _:
        print("未知格式")

简单值匹配（如菜单选项）            ✅ match x: case 'A': ...
多值匹配	                         ✅ `case 'A'
数据结构匹配（元组、列表、字典）	✅ 超级推荐！这是最大优势！
复杂条件判断	                   ✅ 配合 if 守卫
Python < 3.10	❌ 不能用，改用 if-elif-else
'''   
    
    
    
#s[::-1]#首尾互换
    
#del list1
#list2.index()找索引.count()统计

    
    
    
##########################################################
#列表的遍历   
#for i in range (0,len()):
 #   for index,item  in enumerate(list,start=...): #输出序号和值


####################################################################

lst=['qw','er','rt','ty','ui']
print(lst,id(lst))
lst.append('op')
lst.insert(1, 'as')
lst.remove('qw')
lst.pop(3)
lst.clear()#清空
lst.reverse()#列表的反向
lst1=lst.copy()#列表的复制
#lst.sort(reverse=true(降序) or key=str.lower)

newlst=sorted(lst,key=str.lower)


##################################################################
import numpy
import datascience
import matplotlib.pyplot as plt 



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

















