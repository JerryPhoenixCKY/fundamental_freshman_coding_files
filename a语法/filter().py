# ✅ 一、filter() 是什么？
#
# filter() 是 Python 的内置函数，用于过滤序列（如列表、元组等）中的元素，只保留满足条件的元素。
# 📌 作用：从可迭代对象中“筛选”出符合条件的项。
#
# ✅ 二、语法
#
# python
# filter(function, iterable)
#
# 参数 说明
# ------ ------
# function 一个判断函数（返回 True 或 False）<br>如果为 None，则过滤掉所有“假值”（如 0, '', None, False 等）
# iterable 可迭代对象（如 list, tuple, str 等）
# ⚠️ filter() 返回的是一个 filter 对象（迭代器），不是列表！
# 要查看内容，需用 list()、for 循环或解包。
#
# ✅ 三、基本用法示例
# 示例 1：筛选偶数（你的例子）
# python
# numbers = [1, 2, 3, 4, 5, 6]
# evens = list(filter(lambda x: x % 2 == 0, numbers))
# print(evens) # 输出: [2, 4, 6]
# lambda x: x % 2 == 0 是一个匿名函数，判断是否为偶数
# filter 返回迭代器，用 list() 转成列表
# 示例 2：用普通函数代替 lambda
# python
# def is_even(x):
# return x % 2 == 0
#
# evens = list(filter(is_even, numbers))
# print(evens) # [2, 4, 6]
# 示例 3：过滤字符串中的非空项
# python
# words = ["apple", "", "banana", None, "cherry", 0]
# non_empty = list(filter(None, words))
# print(non_empty) # ['apple', 'banana', 'cherry']
# ✅ 当 function=None 时，filter 自动过滤掉“假值”
# 示例 4：过滤正数
# python
# nums = [-3, -1, 0, 2, 5]
# positives = list(filter(lambda x: x > 0, nums))
# print(positives) # [2, 5]
#
# ✅ 四、filter vs 列表推导式（List Comprehension）
#
# Python 中更“Pythonic”的写法通常是列表推导式：
#
# python
# 使用 filter
# evens = list(filter(lambda x: x % 2 == 0, numbers))
# 使用列表推导式（推荐！）
# evens = [x for x in numbers if x % 2 == 0]
#
# ✅ 为什么推荐列表推导式？
# 更易读
# 速度通常更快
# 不需要 lambda 或额外函数
# 💡 Guido van Rossum（Python 之父）曾表示：filter 和 map 在有列表推导式的情况下显得多余。
#
# ✅ 五、常见错误
# ❌ 错误 1：拼写错误
# python
# evens = fliter(lambda x: x % 2 == 0, numbers) # NameError!
# 🔧 修正：filter（f-i-l-t-e-r）
# ❌ 错误 2：忘记转成 list
# python
# evens = filter(lambda x: x % 2 == 0, numbers)
# print(evens) # <filter object at 0x...>
# 🔧 修正：用 list(evens) 或 for x in evens:
# ❌ 错误 3：函数返回非布尔值（虽然不会报错，但逻辑可能错）
# python
# 错误示例：返回数字而不是 True/False
# evens = filter(lambda x: x % 2, numbers) # 这会保留奇数！
# ✅ 正确：x % 2 == 0（明确返回布尔值）
#
# ✅ 六、高级用法：结合其他函数
# 过滤字典列表
# python
# students = [
# {"name": "Alice", "score": 85},
# {"name": "Bob", "score": 70},
# {"name": "Charlie", "score": 90}
# ]
#
# high_scorers = list(filter(lambda s: s["score"] > 80, students))
# print(high_scorers)
# [{'name': 'Alice', 'score': 85}, {'name': 'Charlie', 'score': 90}]
#
# ✅ 总结
#
# 项目 说明
# ------ ------
# 函数名 filter（不是 fliter！）
# 作用 过滤可迭代对象中的元素
# 返回值 filter 对象（迭代器）
# 常用搭配 lambda 表达式 或 普通函数
# 替代方案 列表推导式 [x for x in ... if ...]（更推荐）
# 典型场景 筛选偶数、正数、非空字符串、满足条件的对象等
