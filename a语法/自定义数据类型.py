#初始方法
import math

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_to_origin(self):
        return math.sqrt(self.x**2 + self.y**2)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"Point({self.x}, {self.y})"

# 使用
p = Point(3, 4)
print(p)                     # Point(3, 4)
print(p.distance_to_origin())  # 5.0
p.move(1, 1)
print(p)                     # Point(4, 5)


###################################################################################

class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")
p.age = 30          # 动态添加属性
print(p.age)        # 30

# 其他实例没有这个属性
p2 = Person("Bob")
# print(p2.age)     # AttributeError!

# 2. 为实例动态绑定方法

import types

def walk(self):
    print(f"{self.name} is walking.")

p = Person("Alice")
p.walk = types.MethodType(walk, p)  # 绑定为实例方法
p.walk()  # 输出: Alice is walking.

# p2 没有 walk 方法
p2 = Person("Bob")
# p2.walk()  # AttributeError!