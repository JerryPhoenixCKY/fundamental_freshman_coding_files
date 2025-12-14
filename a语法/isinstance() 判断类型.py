class Fruit:
    pass

class Apple(Fruit):
    def make_cider(self):
        return "Apple cider made!"

class Orange(Fruit):
    def make_juice(self):
        return "Orange juice made!"

class GoldenDelicious(Apple):
    pass

golden = GoldenDelicious()
orange = Orange()

print(isinstance(golden, Fruit))        # True
print(isinstance(golden, Apple))        # True
print(isinstance(golden, GoldenDelicious))  # True
print(isinstance(orange, Apple))        # False

# 安全调用方法
if isinstance(golden, Apple):
    print(golden.make_cider())  # 可以调用
# isinstance() 和 issubclass() 是 Python 中用于类型检查的两个内置函数，常用于调试、API 设计、框架开发等场景。下面详细解释它们的用法、区别和实际示例。
#
# ✅ 一、isinstance(obj, class_or_tuple) —— 检查对象是否是某个类的实例
# 🔹 作用
# 判断 一个对象（obj）是否是指定类（或其子类）的实例。
# 🔹 语法
# python
# isinstance(obj, class)
# 或
# isinstance(obj, (ClassA, ClassB, ...)) # 检查是否属于多个类之一
# 🔹 示例
#
# python
# class Animal:
# pass
#
# class Dog(Animal):
# pass
#
# d = Dog()
#
# print(isinstance(d, Dog)) # True → d 是 Dog 的实例
# print(isinstance(d, Animal)) # True → Dog 继承自 Animal，所以也是 Animal 的实例
# print(isinstance(d, str)) # False
# print(isinstance(42, int)) # True
# print(isinstance("hello", (int, str))) # True → 属于 (int, str) 中的 str
# 🔹 在你代码中的含义：
# python
# isinstance(logger, LoggerBase) # True
#
# → 表示变量 logger 是 LoggerBase 类（或其子类）的一个实例对象。
# ✅ 这常用于：
# 确保传入的参数是预期类型的对象
# 安全调用方法前做类型检查（如 if isinstance(logger, LoggerBase): logger.log(...)）
#
# ✅ 二、issubclass(class, class_or_tuple) —— 检查类是否是另一个类的子类
# 🔹 作用
# 判断 一个类（class）是否是另一个类（或元组中某个类）的子类（包括直接或间接继承）。
# 🔹 语法
# python
# issubclass(ClassA, ClassB)
# 或
# issubclass(ClassA, (ClassX, ClassY, ...))
# 🔹 示例
#
# python
# class A: pass
# class B(A): pass
# class C(B): pass
# class D: pass
#
# print(issubclass(B, A)) # True → B 继承自 A
# print(issubclass(C, A)) # True → C 通过 B 间接继承 A
# print(issubclass(A, A)) # True → 类自身也被视为子类（Python 规定）
# print(issubclass(D, A)) # False
# print(issubclass(C, (A, D))) # True → C 是 A 的子类（满足元组中一个即可）
# 🔹 在你代码中的含义：
# python
# issubclass(FancyConsoleLogger, ConsoleLogger) # True
#
# → 表示 FancyConsoleLogger 类继承自 ConsoleLogger（可能是直接或间接）。
# ✅ 这常用于：
# 框架中验证插件是否符合接口规范
# 动态加载类时检查兼容性
#
# 🔁 三、关键区别总结
#
# 特性 isinstance(obj, cls) issubclass(cls1, cls2)
# ------ ------------------------ --------------------------
# 检查对象 一个实例对象（如 logger） 一个类（如 FancyConsoleLogger）
# 检查目标 是否是某类的实例 是否是某类的子类
# 典型用途 “这个对象能用吗？” “这个类符合接口吗？”
# 参数类型 第一个参数是对象 第一个参数是类
# ❗ 常见错误：
# python
# isinstance(FancyConsoleLogger, ConsoleLogger) # ❌ 错！FancyConsoleLogger 是类，不是实例
# issubclass(logger, LoggerBase) # ❌ 错！logger 是对象，不是类
#
# 🧪 四、实际应用场景
# 场景 1：日志系统（如你的例子）
# python
# def setup_logger(logger):
# if not isinstance(logger, LoggerBase):
# raise TypeError("logger must be an instance of LoggerBase")
# logger.log("System started")
# 场景 2：插件系统
# python
# def register_handler(handler_class):
# if not issubclass(handler_class, BaseHandler):
# raise TypeError("Handler must inherit from BaseHandler")
# # 安全地实例化
# handler = handler_class()
# 场景 3：安全类型转换
# python
# def process_data(data):
# if isinstance(data, str):
# return data.upper()
# elif isinstance(data, (int, float)):
# return data * 2
# else:
# return "Unsupported type"
#
# 💡 五、高级技巧
# 1. 检查抽象基类（ABC）
# python
# from collections.abc import Iterable
# print(isinstance([1,2,3], Iterable)) # True
# print(isinstance("abc", Iterable)) # True
# 2. 自定义 __instancecheck__（极少用）
# 可通过元类自定义 isinstance 行为（一般不需要）。
#
# ✅ 总结口诀
# isinstance 看“对象”是不是某类的“儿子”
# issubclass 看“类”是不是某类的“后代”
# 对象用 isinstance，类用 issubclass


