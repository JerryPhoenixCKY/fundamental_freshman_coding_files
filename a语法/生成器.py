def echo():
     while True:
        received = yield
        print("收到:", received)


g = echo()
next(g)  # 启动生成器，停在 yield 处
g.send("hello")  # 输出: 收到: hello
g.send("world")  # 输出: 收到: world



def echo():
    while True:
        msg = yield "等待输入..."
        print("你说了：", msg)

g = echo()
next(g)
g.send("Hello")      # 传字符串
g.send(42)           # 也可以中途传整数！
g.send([1, 2, 3])    # 甚至传列表

def fib(a,b):
    while True:
        c=a+b
        yield c
x=int(input())
y=int(input())
q=fib(x,y)
q.send('q')
for i in q:
    print(i,end=" ")

ans = 0

def fib(a,b):
    global ans
    while b<100:
        c=a+b
        ans = ans + 1
        print("turn %d: " % ans, end="")
        temp = yield c
        print("temp equals to %d " % temp)
        a=b
        b=c

x=int(input())
y=int(input())
fib_gen = fib(x,y)
next(fib_gen)
i = 1
while True:
    try:
        print(i, end="\n")
        i += 1
        print("send %d to generator" % (i - 10))
        fib_gen.send(i - 10)
    except StopIteration:
        print("迭代完成")
        break