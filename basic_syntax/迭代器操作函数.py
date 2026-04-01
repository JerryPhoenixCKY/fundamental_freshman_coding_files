numbers = [1, 2, 3, 4]
squared = map(lambda x: x ** 2, numbers)#lambda是匿名函数
print(list(squared))  # [1, 4, 9, 16]

list1 = [1, 2, 3]
list2 = [10, 20, 30]

# 将两个列表对应元素相加
result = map(lambda x, y: x + y, list1, list2)
print(list(result))  # [11, 22, 33]


# 转换字符串为整数
str_nums = ['1', '2', '3']
int_nums = map(int, str_nums)
print(list(int_nums))  # [1, 2, 3]

# 获取每个字符串的长度
words = ['apple', 'banana', 'cherry']
lengths = map(len, words)
print(list(lengths))  # [5, 6, 6]

#结合了operate模块
from operator import add, mul
a = [1, 2, 3]
b = [4, 5, 6]
# 相加
print(list(map(add, a, b)))  # [5, 7, 9]
# 相乘
print(list(map(mul, a, b)))  # [4, 10, 18]

# 2. 与 itertools 结合处理流数据
import itertools

# 无限序列：对前 5 个偶数平方
evens = itertools.count(0, 2)  # 0, 2, 4, 6, ...
squares = map(lambda x: x**2, evens)
first_five = list(itertools.islice(squares, 5))
print(first_five)  # [0, 4, 16, 36, 64]




def fib(a,b):
    while b<100:
        c=a+b
        yield c
        a=b
        b=c
x=int(input())
y=int(input())
for i in fib(x,y):
    print(i,end=" ")



# 在 Python 中，迭代器（Iterator）是一种可以被 `next()` 函数调用并不断返回下一个值的对象。
## 一、内置函数（Built-in Functions）
# ### 1. `iter(iterable)`
# - 将一个可迭代对象（如列表、元组、字符串等）转换为迭代器。
# - 也可用于自定义迭代协议（传入 `__iter__` 和 `__next__` 方法）。
#
# python
# it = iter([1, 2, 3])
# print(next(it))  # 1
# ### 2. `next(iterator[, default])`
# - 获取迭代器的下一个元素。
# - 如果迭代器耗尽，且提供了 `default`，则返回 `default`；否则抛出 `StopIteration`。
#
# ```python
# it = iter([1, 2])
# print(next(it))        # 1
# print(next(it))        # 2
# print(next(it, 'end')) # 'end'
# ```
#
#3. `enumerate(iterable, start=0)`
# - 返回一个枚举迭代器，每个元素是 `(index, value)` 的元组。
#
# ```python
# for i, v in enumerate(['a', 'b']):
#     print(i, v)
# # 输出：
# # 0 a
# # 1 b

# ### 4. `zip(*iterables)`
# - 将多个可迭代对象“压缩”成一个迭代器，每次返回一个由各输入元素组成的元组。
#
# ```python
# list(zip([1, 2], ['a', 'b']))  # [(1, 'a'), (2, 'b')]
# ```
#
# ### 5. `map(function, iterable, ...)`
# - 将函数应用于每个元素，返回一个 map 对象（迭代器）。
#
# ```python
# list(map(str, [1, 2, 3]))  # ['1', '2', '3']
# ```
#
# ### 6. `filter(function, iterable)`
# - 过滤出使函数返回 `True` 的元素，返回一个 filter 对象（迭代器）。
#
# ```python
# list(filter(lambda x: x > 0, [-1, 0, 1, 2]))  # [1, 2]
# ```
#
# ### 7. `reversed(seq)`
# - 返回一个反向迭代器（要求 `seq` 是序列，如 list、str、tuple）。
#
# ```python
# list(reversed([1, 2, 3]))  # [3, 2, 1]
# ```
#
# ### 8. `sorted(iterable, *, key=None, reverse=False)`
# - 虽然返回的是列表，但输入可以是任意可迭代对象。
#
# ---
#
# ## 二、`itertools` 模块中的迭代器函数（需 `import itertools`）
#
# `itertools` 是 Python 标准库中专门用于高效迭代操作的模块。
#
# ### 常用函数：
#
# | 函数 | 功能 |
# |------|------|
# | `itertools.count(start=0, step=1)` | 无限计数器 |
# | `itertools.cycle(iterable)` | 无限循环迭代 |
# | `itertools.repeat(object[, times])` | 重复对象 |
# | `itertools.chain(*iterables)` | 串联多个迭代器 |
# | `itertools.islice(iterable, start, stop[, step])` | 对迭代器切片（类似 `list[start:stop:step]`） |
# | `itertools.tee(iterable, n=2)` | 将一个迭代器复制成 n 个独立的迭代器 |
# | `itertools.zip_longest(*iterables, fillvalue=None)` | 类似 `zip`，但以最长为准，不足用 `fillvalue` 填充 |
# | `itertools.product(*iterables, repeat=1)` | 笛卡尔积 |
# | `itertools.permutations(iterable, r=None)` | 排列 |
# | `itertools.combinations(iterable, r)` | 组合 |
# | `itertools.groupby(iterable, key=None)` | 按 key 分组（注意：需先排序） |
#
# #### 示例：
#
# ```python
# import itertools
#
# # 无限计数
# counter = itertools.count(10, 2)
# print(next(counter))  # 10
# print(next(counter))  # 12
#
# # 链接多个列表
# for x in itertools.chain([1, 2], [3, 4]):
#     print(x)  # 1, 2, 3, 4
#
# # 切片迭代器（避免转成 list）
# it = iter(range(100))
# first_five = list(itertools.islice(it, 5))  # [0, 1, 2, 3, 4]
# ```
#
# ---
#
# ## 三、其他实用技巧
#
# ### 1. 检查是否为迭代器
# ```python
# from collections.abc import Iterator, Iterable
#
# isinstance(iter([1,2]), Iterator)   # True
# isinstance([1,2], Iterator)         # False
# isinstance([1,2], Iterable)         # True
# ```
#
# ### 2. 消费迭代器（一次性使用）
# 迭代器只能遍历一次，再次使用需重新创建。
#
# ```python
# it = iter([1, 2, 3])
# list(it)  # [1, 2, 3]
# list(it)  # []  ← 已耗尽
