# 二、`itertools` 模块：高效迭代工具
#
# `itertools` 提供了一系列用于**创建和操作迭代器**的函数，特别适合处理大数据流、组合问题、无限序列等场景。所有函数都返回**迭代器**（惰性求值），内存效率极高。
#
# 模块分为三类：
# 1. **无限迭代器**
# 2. **有限迭代器**
# 3. **组合生成器**
#
# ---
#
# ### 1. 无限迭代器（需手动终止）
#
# | 函数 | 说明 | 示例 |
# |------|------|------|
# | `count(start=0, step=1)` | 无限计数 | `count(10, 2) → 10, 12, 14, ...` |
# | `cycle(iterable)` | 无限循环迭代 | `cycle('AB') → A, B, A, B, ...` |
# | `repeat(object[, times])` | 重复对象 | `repeat(5, 3) → 5, 5, 5` |
#
# ```python
# from itertools import count, cycle, repeat
#
# # 生成带索引的数据
# for i, char in zip(count(1), 'abc'):
#     print(i, char)  # 1 a, 2 b, 3 c
#
# # 重复填充
# list(repeat('x', 4))  # ['x', 'x', 'x', 'x']
# ```
#
# ---
#
# ### 2. 有限迭代器（处理现有迭代器）
#
# | 函数 | 说明 | 示例 |
# |------|------|------|
# | `chain(*iterables)` | 串联多个迭代器 | `chain([1,2], [3,4]) → 1,2,3,4` |
# | `islice(iterable, start, stop[, step])` | 对迭代器切片 | `islice(count(), 5) → 0,1,2,3,4` |
# | `tee(iterable, n=2)` | 复制迭代器为 n 个独立副本 | `it1, it2 = tee([1,2,3])` |
# | `zip_longest(*iterables, fillvalue=None)` | 类似 `zip`，但以最长为准 | `zip_longest('AB', '123', fillvalue='-') → ('A','1'), ('B','2'), ('-','3')` |
#
# ```python
# from itertools import chain, islice
#
# # 合并多个文件行
# lines = chain(open('file1.txt'), open('file2.txt'))
#
# # 取前 10 行
# first_10 = list(islice(lines, 10))
# ```
#
# ---
#
# ### 3. 组合生成器（排列组合）
#
# | 函数 | 说明 | 示例 |
# |------|------|------|
# | `product(*iterables, repeat=1)` | 笛卡尔积 | `product('AB', '12') → ('A','1'), ('A','2'), ('B','1'), ('B','2')` |
# | `permutations(iterable, r=None)` | 排列（不重复） | `permutations('ABC', 2) → ('A','B'), ('A','C'), ('B','A'), ...` |
# | `combinations(iterable, r)` | 组合（无序，不重复） | `combinations('ABC', 2) → ('A','B'), ('A','C'), ('B','C')` |
# | `combinations_with_replacement(iterable, r)` | 组合（允许重复） | `combinations_with_replacement('AB', 2) → ('A','A'), ('A','B'), ('B','B')` |
#
# ```python
# from itertools import product, combinations
#
# # 生成所有可能的密码组合
# for pwd in product('01', repeat=3):
#     print(''.join(pwd))  # 000, 001, 010, ..., 111
#
# # 从 5 个数中选 3 个组合
# list(combinations([1,2,3,4,5], 3))
# ```
#
# ---
#
# ### 4. 其他实用函数
#
# | 函数 | 说明 |
# |------|------|
# | `groupby(iterable, key=None)` | 按 key 分组（**注意：需先排序！**） |
# | `accumulate(iterable, func=operator.add)` | 累积计算（如前缀和） |
#
# ```python
# from itertools import groupby, accumulate
# from operator import add
#
# # 累积求和
# list(accumulate([1, 2, 3, 4]))  # [1, 3, 6, 10]
#
# # 分组（必须先排序！）
# data = [('a', 1), ('a', 2), ('b', 3), ('a', 4)]
# # 先按 key 排序
# data.sort(key=lambda x: x[0])
# for key, group in groupby(data, key=lambda x: x[0]):
#     print(key, list(group))
# # a [('a', 1), ('a', 2), ('a', 4)]
# # b [('b', 3)]
# ```
#
# ---
#
# ## 三、`operator` + `itertools` 联合使用示例
#
# ```python
# from itertools import starmap
# from operator import mul
#
# # 对元组列表中的每对数相乘
# pairs = [(2, 3), (4, 5), (6, 7)]
# result = list(starmap(mul, pairs))  # [6, 20, 42]
#
# # 等价于：
# # [mul(a, b) for a, b in pairs]
# # 或
# # [a * b for a, b in pairs]
# ```
#
# > `starmap(func, iterable)` 相当于 `map(func, *zip(*iterable))`，适用于参数已打包为元组的情况。
