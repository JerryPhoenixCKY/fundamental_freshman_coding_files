print(dir(object))

# 方法	说明	触发方式	示例
# __new__(cls, ...)	创建对象实例（静态方法）	MyClass()	见下文
# __init__(self, ...)	初始化对象	MyClass()	def __init__(self, name): self.name = name
# __del__(self)	析构函数（不保证调用）	对象被销毁时	少用，推荐用 with 或显式清理
# __repr__(self)	“官方”字符串表示，用于调试	repr(obj) 或交互式解释器	return f"MyClass({self.name!r})"
# __str__(self)	“用户友好”字符串表示	str(obj) 或 print(obj)	return f"Name: {self.name}"
# __eq__(self, other)	等于比较	a == b	return self.id == other.id
# __ne__(self, other)	不等于（Python 3 中可省略）	a != b	默认为 not (a == b)
# __lt__, __le__, __gt__, __ge__	比较运算符	a < b, a >= b 等	实现排序逻辑
# __hash__(self)	返回哈希值	hash(obj)，用于 dict/set	若定义 __eq__ 且对象可变，应设为 None
# __bool__(self)	布尔值（真/假）	bool(obj) 或 if obj:	return self.value > 0
# __getattr__(self, name)	访问不存在的属性时调用	obj.xxx（xxx 不存在）	动态属性代理
# __getattribute__(self, name)	所有属性访问都调用（慎用）	obj.any_attr	高级拦截，易引发递归
# __setattr__(self, name, value)	设置属性时调用	obj.x = 1	属性验证、日志等
# __delattr__(self, name)	删除属性时调用	del obj.x	安全删除控制
# __dir__(self)	自定义 dir(obj) 的结果	dir(obj)	返回属性列表
# __class__	对象的类（不是方法，是属性）	obj.__class__	等价于 type(obj)
# __doc__	文档字符串	MyClass.__doc__	类或方法的 docstring
# __format__(self, format_spec)	格式化字符串	f"{obj:spec}" 或 format(obj, spec)	自定义格式行为
# __sizeof__(self)	对象内存大小（字节）	sys.getsizeof(obj)	调试内存使用
# __reduce__, __reduce_ex__	支持 pickle 序列化	pickle.dumps(obj)	自定义序列化逻辑
# __init_subclass__(cls, **kwargs)	子类被创建时调用（Python 3.6+）	class Child(Parent, kw=...):	替代部分元类功能
# __subclasshook__(cls, subclass)	自定义 issubclass() 行为（配合 ABC）	issubclass(A, B)	用于抽象基类协议

# new vs init

class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # True

# __str__ 和 __repr__

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __str__(self):
        return f"Point at ({self.x}, {self.y})"
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(1, 2)
print(p)        # Point at (1, 2)  ← __str__
print(repr(p))  # Point(1, 2)     ← __repr__
# 3. 比较方法（__eq__, __lt__ 等）
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __eq__(self, other):
        return self.age == other.age
    def __lt__(self, other):
        return self.age < other.age

p1 = Person("Alice", 30)
p2 = Person("Bob", 25)
print(p1 > p2)  # True

# 4. __hash__ 与可哈希性

class ImmutablePoint:
    def __init__(self, x, y):
        self._x, self._y = x, y
    def __hash__(self):
        return hash((self._x, self._y))
    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

p = ImmutablePoint(1, 2)
s = {p}  # 可放入 set
# ❌ 如果对象可变（如 list），不应定义 __hash__，或设为 None：


class Mutable:
    __hash__ = None  # 明确禁止哈希

# 5. __setattr__ 控制属性赋值

class Strict:
    def __setattr__(self, name, value):
        if name.startswith('_'):
            raise AttributeError("Private attributes not allowed")
        super().__setattr__(name, value)

s = Strict()
s.name = "OK"      # ✅
# s._secret = 1    # ❌ 报错

# 6. __init_subclass__ 替代简单元类

class Register:
    subclasses = []
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Register.subclasses.append(cls)

class A(Register): pass
class B(Register): pass

print(Register.subclasses)  # [<class '__main__.A'>, <class '__main__.B'>]