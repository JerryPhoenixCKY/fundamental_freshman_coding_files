# ## 一、`operator` 模块：函数式操作内置运算
#
# `operator` 模块提供了一组与 Python 内置运算符（如 `+`, `-`, `[]`, `in` 等）对应的**函数**，使得你可以将运算符当作函数传递（例如用于 `map`, `reduce`, `sorted` 等高阶函数）。
#
# ### ✅ 为什么需要 `operator`？
# - 避免写冗余的 `lambda` 表达式
# - 提高性能（C 实现）
# - 代码更清晰、更函数式
#
# ---
#
# ### 常用函数示例
#
# | 运算 | `operator` 函数 | 等价表达式 |
# |------|------------------|-----------|
# | `a + b` | `operator.add(a, b)` | `lambda a, b: a + b` |
# | `a - b` | `operator.sub(a, b)` | `lambda a, b: a - b` |
# | `a * b` | `operator.mul(a, b)` | `lambda a, b: a * b` |
# | `a / b` | `operator.truediv(a, b)` | `lambda a, b: a / b` |
# | `a // b` | `operator.floordiv(a, b)` | `lambda a, b: a // b` |
# | `a % b` | `operator.mod(a, b)` | `lambda a, b: a % b` |
# | `a ** b` | `operator.pow(a, b)` | `lambda a, b: a ** b` |
# | `-a` | `operator.neg(a)` | `lambda a: -a` |
# | `a < b` | `operator.lt(a, b)` | `lambda a, b: a < b` |
# | `a <= b` | `operator.le(a, b)` | `lambda a, b: a <= b` |
# | `a == b` | `operator.eq(a, b)` | `lambda a, b: a == b` |
# | `a != b` | `operator.ne(a, b)` | `lambda a, b: a != b` |
# | `a in b` | `operator.contains(b, a)` | `lambda a, b: a in b` |
#
# #### 属性/项访问
# | 表达式 | `operator` 函数 |
# |--------|----------------|
# | `obj.attr` | `operator.attrgetter('attr')` |
# | `obj[key]` | `operator.itemgetter(key)` |
# | `obj.method()` | `operator.methodcaller('method')` |
#
# ---
#
# ### 实际应用场景
#
# #### 1. 替代 lambda（更高效、更清晰）
#
# ```python
# from operator import add, mul
#
# # 使用 map
# numbers = [1, 2, 3, 4]
# print(list(map(add, numbers, [10]*4)))  # [11, 12, 13, 14]
#
# # 使用 reduce
# from functools import reduce
# product = reduce(mul, [1, 2, 3, 4])  # 24
# ```
#
# #### 2. 排序（替代 lambda）
#
# ```python
# students = [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
#
# # 按成绩排序（等价于 key=lambda x: x[1]）
# from operator import itemgetter
# sorted_students = sorted(students, key=itemgetter(1))
#
# # 按多个字段排序：先按成绩降序，再按姓名升序
# sorted_students = sorted(students, key=itemgetter(1, 0), reverse=True)
# # 注意：reverse 会影响所有字段，若需混合排序，需用负号或自定义 key
# ```
#
# #### 3. 访问对象属性
#
# ```python
# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
# people = [Person('Alice', 30), Person('Bob', 25)]
#
# # 按 age 排序
# from operator import attrgetter
# sorted_people = sorted(people, key=attrgetter('age'))
# ```
#
# #### 4. 调用方法
#
# ```python
# words = ['hello', 'WORLD', 'Python']
# # 调用每个字符串的 .lower() 方法
# from operator import methodcaller
# lower_words = list(map(methodcaller('lower'), words))
# # ['hello', 'world', 'python']
# ```
#
# ---
#

