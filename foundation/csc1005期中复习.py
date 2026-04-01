# 核心特征
#
# 程序与数据统一存储
# 指令（程序）和数据存放在同一个读写存储器（内存）中。
# CPU 无法从形式上区分某段二进制是“指令”还是“数据”，仅根据上下文解释。
# 五大基本组成部分
# 运算器（ALU, Arithmetic Logic Unit）：执行算术与逻辑运算。
# 控制器（CU, Control Unit）：从内存取指令、译码并协调各部件执行。
# 存储器（Memory）：线性编址，存储程序和数据。
# 输入设备（Input）：如键盘、传感器等。
# 输出设备（Output）：如显示器、打印机等。
# 顺序执行 + 指令指针
# 程序默认按内存地址顺序执行。
# 通过程序计数器（PC, Program Counter）指向下一条要执行的指令地址。
# 支持跳转、循环、函数调用等控制流（通过修改 PC 实现）。
# 二进制编码
# 所有信息（指令、数据、地址）均以二进制形式表示和处理。


# NRZL    是1才变
# NRZI   当数据位为1时，信号发生翻转；当数据位为0时，信号保持不变

# 特性	   str	  dict	   list	  tuple
# 可变	    ❌	   ✅       ✅	   ❌
# 有序   	✅	   ✅	    ✅     ✅
# 重复元素	✅	   ❌ 	    ✅	   ✅
# 索引访问	✅	❌（用 key）	✅	   ✅
# 切片	    ✅	   ❌      	✅     ✅
# 常用操作 文本处理  查找/映射 增删改	  固定结构



# 进制转化
# 将记录的余数逆序排列，即为目标进制的整数部分。
# 将记录的整数部分按顺序排列，即为目标进制的小数部分。
# ️注意：某些十进制小数在目标进制下可能无法精确表示（如十进制 0.1 转二进制是无限循环），需根据精度要求截断或标注循环。
# 方法：
# 整数部分：从小数点向左分组，不足补前导零
# 小数部分：从小数点向右分组，不足补后缀零
# 每组直接查表转换
# 其他进制对（如 3↔9、4↔16）也可类似处理，但非常用。
# 四、总结流程图
# 源进制数（含小数）
# ↓
# [按权展开] → 十进制数（整数 + 小数）
# ↓
# [整数：除基取余] → 目标进制整数部分
# [小数：乘基取整] → 目标进制小数部分
# ↓
# 拼接 → 目标进制数

# 一、str（字符串）——不可变、文本处理主力
# 字符串是不可变序列，所有“修改”操作都会返回新字符串，原字符串不变。
#
# 方法	功能说明	示例
# .upper()	转为大写	"hello".upper() → "HELLO"
# .lower()	转为小写	"HELLO".lower() → "hello"
# .capitalize()	首字母大写，其余小写	"hello world".capitalize() → "Hello world"
# .title()	每个单词首字母大写	"hello world".title() → "Hello World"
# .strip()	去除首尾空白（或指定字符）	"  hi  ".strip() → "hi"
# .lstrip() / .rstrip()	去左/右空白	"  hi".lstrip() → "hi"
# .split(sep)	按分隔符拆成列表（默认空格）	"a,b,c".split(',') → ['a', 'b', 'c']
# .join(iterable)	用当前字符串连接可迭代对象	'-'.join(['a','b']) → 'a-b'
# .replace(old, new)	替换子串	"apple".replace('p', 'x') → "axxle"
# .find(sub)	查找子串位置，找不到返回 -1	"hello".find('e') → 1
# .index(sub)	类似 find，但找不到会报错	"hello".index('x') → ValueError
# .startswith(prefix)	是否以某字符串开头	"file.txt".startswith("file") → True
# .endswith(suffix)	是否以某字符串结尾	"file.txt".endswith(".txt") → True
# .isdigit() / .isalpha() / .isalnum()	判断是否全为数字/字母/字母数字	"123".isdigit() → True
# 💡 注意：字符串方法不会改变原字符串！
#
# s = "hello"
# s.upper()  # 返回 "HELLO"，但 s 仍是 "hello"
# s = s.upper()  # 必须重新赋值才能“修改”
# 二、dict（字典）——键值对映射，查找快
# 字典是可变、无序（但 Python 3.7+ 保留插入顺序）的键值对集合，键必须是不可变类型（如 str, int, tuple）。
#
# 方法	功能说明	示例
# .keys()	返回所有键的视图（类似列表）	d.keys() → dict_keys(['a', 'b'])
# .values()	返回所有值的视图	d.values() → dict_values([1, 2])
# .items()	返回所有**(键, 值)** 对的视图	d.items() → dict_items([('a',1), ('b',2)])
# .get(key, default)	安全取值，键不存在返回 default（默认 None）	d.get('c', 0) → 0（若 'c' 不存在）
# .update(other)	用另一个字典更新当前字典（覆盖或新增）	d.update({'a':10, 'c':3})
# .pop(key)	删除并返回对应值，键不存在会报错	d.pop('a') → 1
# .pop(key, default)	安全删除，不存在返回 default	d.pop('x', -1) → -1
# .clear()	清空字典	d.clear() → {}
# del d[key]	删除键值对（不是方法，但常用）	del d['a']
# .setdefault(key, default)	若 key 不存在，设为 default 并返回；否则返回原值	d.setdefault('c', 0) → 若 'c' 不存在，则 d['c']=0
# 💡 重要：
#
# 遍历字典默认遍历键：for k in d: ...
# 用 .items() 同时取键和值：for k, v in d.items(): ...
# 三、list（列表）——可变序列，功能最全
# 列表是可变、有序的序列，支持增删改查，是最常用的容器。
#
# 方法	功能说明	示例
# .append(x)	在末尾添加一个元素	lst.append(4) → [1,2,3,4]
# .extend(iterable)	在末尾添加多个元素（展开 iterable）	lst.extend([4,5]) → [1,2,3,4,5]
# .insert(i, x)	在索引 i 处插入元素 x	lst.insert(1, 9) → [1,9,2,3]
# .remove(x)	删除第一个值为 x 的元素，不存在报错	lst.remove(2)
# .pop()	删除并返回最后一个元素	lst.pop() → 3（原列表变 [1,2]）
# .pop(i)	删除并返回索引 i 处的元素	lst.pop(0) → 1
# .clear()	清空列表	lst.clear() → []
# .index(x)	返回第一个 x 的索引，不存在报错	[1,2,3].index(2) → 1
# .count(x)	统计 x 出现次数	[1,1,2].count(1) → 2
# .sort()	原地排序（升序），可加 reverse=True	lst.sort(reverse=True)
# .reverse()	原地反转列表	[1,2,3].reverse() → [3,2,1]
# del lst[i]	删除索引 i 处元素（不是方法）	del lst[0]
# lst[i] = x	修改索引 i 处的值	lst[0] = 99
# 💡 注意：
#
#
# .sort() 和 .reverse() 会修改原列表，不返回新列表！
# 若想“不修改原列表排序”，用 sorted(lst)（返回新列表）
# 四、tuple（元组）——不可变序列，轻量安全
# 元组是不可变、有序的序列，一旦创建不能增删改元素（但内部可变对象内容可变）。
#
# 方法	功能说明	示例
# .count(x)	统计 x 出现次数	(1,2,2).count(2) → 2
# .index(x)	返回第一个 x 的索引，不存在报错	(1,2,3).index(2) → 1
# ❗ 元组没有 .append(), .pop(), .sort() 等方法！
#
#
# 因为它是不可变的，所以只提供查询类方法。
#
# 💡 但你可以：
# 用 + 拼接生成新元组：(1,2) + (3,) → (1,2,3)
# 用 * 重复：(1,) * 3 → (1,1,1)
# 用 len(), max(), min(), in 等内置函数：2 in (1,2,3) → True



# 一、break：立刻跳出整个循环
# 一旦执行 break，循环马上结束，不再执行后续的循环体，也不再判断条件。
# 常用于：找到目标就停止、遇到错误提前退出。
#
# 二、continue：跳过本次循环，进入下一次
# 执行 continue 后，本次循环剩下的代码不执行，直接开始下一轮循环。
# 常用于：跳过某些特殊情况，比如跳过无效数据、跳过偶数等。
