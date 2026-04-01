
# ✅ 方法 1：使用内置函数 round()
#
# python
# x = 3.1415926
# y = round(x, 2) # 保留 2 位小数
# print(y) # 输出: 3.14
# ⚠️ 注意：round() 使用的是 “银行家舍入法”（四舍六入五成双），在某些边界情况下可能不符合直觉。
# 例如：round(2.5) → 2，round(3.5) → 4
#
# 适用于大多数常规场景，但不适合金融计算等对精度要求极高的场合。
#
# ✅ 方法 2：使用格式化字符串（推荐用于显示）
# 方式 2.1：f-string（Python 3.6+ 推荐）
# python
# x = 3.1415926
# print(f"{x:.2f}") # 输出: 3.14
# 方式 2.2：.format()
# python
# x = 3.1415926
# print("{:.2f}".format(x)) # 输出: 3.14
# 方式 2.3：% 格式化（旧式，不推荐新代码使用）
# python
# x = 3.1415926
# print("%.2f" % x) # 输出: 3.14
# 💡 这些方法返回的是字符串，适合用于输出或打印，不改变原始数值类型。
#
# ✅ 方法 3：使用 decimal 模块（高精度、可控舍入，适合金融）
#
# python
# from decimal import Decimal, ROUND_HALF_UP
#
# x = Decimal('3.1415926')
# y = x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) # 保留两位小数，四舍五入
# print(y) # 输出: 3.14
# print(type(y)) # <class 'decimal.Decimal'>
# ✅ 优点：
# 精确控制舍入方式（如 ROUND_HALF_UP 就是传统四舍五入）
# 避免浮点数精度误差（如 0.1 + 0.2 != 0.3 的问题）
# 📌 注意：应使用字符串初始化 Decimal，避免浮点数传入带来的误差：
# python
# Decimal(0.1) # ❌ 可能引入浮点误差
# Decimal('0.1') # ✅ 正确
#
# ✅ 方法 4：使用 math 模块手动截断或舍入（较少用）
#
# 例如保留 2 位小数（向下截断）：
# python
# import math
# x = 3.1415926
# y = math.floor(x * 100) / 100 # 3.14
#
# 但通常不如上述方法简洁。
#
# 🔍 各方法对比总结
#
# 方法 返回类型 是否真正改变数值 舍入方式 适用场景
# ------ -------- ---------------- -------- --------
# round() float 是 银行家舍入 一般计算
# f"{x:.2f}" str 否 四舍五入（显示时） 打印、输出
# decimal.Decimal Decimal 是 可控（如 ROUND_HALF_UP） 金融、高精度
# math.floor 等 float 是 手动控制 特殊需求
#
# ✅ 推荐做法
# 显示输出 → 用 f"{x:.2f}"
# 一般计算保留小数 → 用 round(x, 2)
# 金融/会计/精确计算 → 用 decimal.Decimal
#
# 示例：综合使用
#
# python
# price = 19.999
# 显示时保留两位小数
# print(f"价格: ¥{price:.2f}") # 价格: ¥20.00
# 真正存储为两位小数（金融）
# from decimal import Decimal, ROUND_HALF_UP
# price_d = Decimal('19.999').quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
# print(price_d) # 20.00

