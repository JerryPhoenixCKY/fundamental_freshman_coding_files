"""
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 ├── GeneratorExit
 └── Exception
      ├── StopIteration
      ├── StopAsyncIteration
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ImportError
      │    └── ModuleNotFoundError  （Python 3.6+）
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    └── RecursionError
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning（及其子类，如 DeprecationWarning, UserWarning 等）


ValueError	函数接收到正确类型但值无效，如 int("abc")
TypeError	操作或函数应用于不适当类型的对象，如 "a" + 1
IndexError	序列下标越界，如 lst = [1]; lst[5]
KeyError	字典中找不到指定键，如 d = {}; d['x']
AttributeError	对象没有指定属性，如 "hello".foo
NameError	使用未定义的变量，如 print(x)（x 未定义）
ZeroDivisionError	除以零，如 1 / 0                               用try except解决
FileNotFoundError	尝试打开不存在的文件，如 open('no.txt')
ImportError / ModuleNotFoundError	导入不存在的模块，如 import nonexistent
OSError	操作系统相关错误（如权限、文件系统等）
AssertionError	assert 语句失败
SyntaxError	代码语法错误（通常在解析时抛出，不能在运行时捕获）
IndentationError	缩进错误（SyntaxError 的子类）
RecursionError	递归深度超过限制



"""



#1try except 排除异常 在except后面要加错误类型
from sys import exception

try:
    num1=int(input('please input a integer：'))
    num2=int(input('please input another integer：'))
    if num2 == 0:
        raise Exception('除数不能为0')

except ValueError:
    print('不能转化字符串')

except Exception as e:
    print(e)

except BaseException:
    print('error')

else:#没有异常时执行
    result=num1/num2
    print('结果',result)
finally:
    print('w无论是否异常finally的代码都会执行')




