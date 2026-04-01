# `lambda` 是 Python 中用于创建匿名函数（即没有名字的函数）的关键字。它适用于编写简单、短小的函数，通常用于需要函数对象但又不想正式定义函数的场合（比如作为参数传给高阶函数）。
#
# ---
#
# ### 1. 基本语法
#
# ```python
# lambda 参数: 表达式
# ```
#
# - **参数**：可以有多个，用逗号分隔。
# - **表达式**：只能是一个表达式，不能是复杂的语句（比如不能包含 `print`、`return`、`if-else` 块等，但可以用条件表达式）。
# - **返回值**：表达式的计算结果自动作为返回值。
#
# ---
#
# ### 2. 示例
#
# #### 简单示例：加法
# ```python
# add = lambda x, y: x + y
# print(add(3, 5))  # 输出: 8
# ```
#
# 等价于：
# ```python
# def add(x, y):
#     return x + y
# ```
#
# #### 用在高阶函数中（如 `map`, `filter`, `sorted`）
#
# - **map** 示例：
#   ```python
#   numbers = [1, 2, 3, 4]
#   squares = list(map(lambda x: x**2, numbers))
#   print(squares)  # [1, 4, 9, 16]
#   ```
#
# - **filter** 示例：
#   ```python
#   numbers = [1, 2, 3, 4, 5, 6]
#   evens = list(filter(lambda x: x % 2 == 0, numbers))
#   print(evens)  # [2, 4, 6]
#   ```
#
# - **sorted** 示例（按字典的某个键排序）：
#   ```python
#   students = [
#       {'name': 'Alice', 'score': 88},
#       {'name': 'Bob', 'score': 92},
#       {'name': 'Charlie', 'score': 75}
#   ]
#   sorted_students = sorted(students, key=lambda x: x['score'])
#   print(sorted_students)
#   # 按分数升序排列
#   ```
#
# ---
#
# ### 3. 注意事项
#
# - **只能写一个表达式**，不能写多行逻辑。
# - **不推荐用于复杂逻辑**，会使代码难以阅读。
# - **没有函数名**，调试时可能不太方便（但可以用 `__name__` 查看，通常显示为 `<lambda>`）。
#
# ---
#
# ### 4. 条件表达式（三元运算）在 lambda 中的使用
#
# ```python
# f = lambda x: "偶数" if x % 2 == 0 else "奇数"
# print(f(4))  # 偶数
# print(f(7))  # 奇数
# ```
#
# ---
#
# ### 5. 何时使用 lambda？
#
# ✅ 适合：
# - 一次性使用的简单函数
# - 作为 `map`、`filter`、`sorted`、`reduce` 等函数的参数
#
# ❌ 不适合：
# - 需要复用的逻辑（应使用 `def` 定义函数）
# - 包含复杂逻辑或多行代码


def fac(n):
    if n==1:
        return 1
    else:
        return n*fac(n-1)

print(fac(6))

# 斐波那契数列
def fun(n):
    if n==1 or n==2:
        return 1
    else:
        return fun(n-1)+fun(n-2)

for i in range(1,11):
    print(fun(i),end='\t')














