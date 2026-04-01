# 判断一段代码的时间复杂度，是算法分析的核心技能。根据你上传的 《Lecture 8: Data Structure and Algorithm》 讲义内容（特别是第 5–12 页关于算法分析、大 O 表示法、基本函数增长阶的部分），我将结合讲义中的原则和实际编程经验，给出一套系统、可操作的判断方法。
#
# ✅ 一、核心思想（来自讲义）
#
# 讲义中强调了三个关键原则：
#
# 1. 计数基本操作（Primitive Operations）
# “We define a set of primitive operations such as: assigning, arithmetic, comparison, list indexing, function call…”
#
# 2. 以输入规模 \( n \) 为变量
# “Associate… a function \( f(n) \) that characterizes the number of primitive operations as a function of the problem size \( n \)”
#
# 3. 关注最坏情况 & 渐进增长（Asymptotic Analysis）
# “Focus on the worst-case input” + “Use Big-Oh to suppress constant factors and lower-order terms”
#
# ✅ 二、判断时间复杂度的 5 步法
# 🔹 第 1 步：确定输入规模 \( n \) 是什么？
# 对于数组/列表 → \( n = \text{len(list)} \)
# 对于矩阵 → \( n = \text{rows} \times \text{cols} \) 或 \( n = \text{边长} \)
# 对于树 → \( n = \text{节点数} \)
# 对于图 → \( n = \text{顶点数} \)，有时也考虑边数 \( m \)
# 📌 关键：找到那个“随着问题变大而增长”的量。
#
# 🔹 第 2 步：识别主导结构（循环、递归）
# 时间复杂度主要由以下结构决定：
#
# 结构 复杂度规律
# ------ ----------
# 单层循环 for i in range(n) \( O(n) \)
# 嵌套循环（两层） \( O(n^2) \)
# 嵌套循环（k 层） \( O(n^k) \)
# 二分查找 / 折半 \( O(\log n) \)
# 递归（每次减半） \( O(\log n) \)
# 递归（分治，如归并排序） \( O(n \log n) \)
# 递归（每个问题分成两个子问题） 可能 \( O(2^n) \)
#
# 🔹 第 3 步：逐行分析 + 累加操作次数
#
# 对每行代码，估算它在最坏情况下执行多少次（用 \( n \) 表示），然后相加。
# 示例 1：线性搜索
# python
# def linear_search(arr, target):
# for i in range(len(arr)): # 执行 n 次
# if arr[i] == target: # 每次 1 次比较 → 共 n 次
# return i
# return -1
# 总操作数 ≈ \( n \)（比较）+ \( n \)（索引）→ \( 2n \)
# 忽略常数 → \( O(n) \)
# 示例 2：冒泡排序（双重循环）
# python
# for i in range(n): # 外层 n 次
# for j in range(n - i): # 内层平均 ~n/2 次 → 总共 ~n²/2 次
# if arr[j] > arr[j+1]:
# swap
# 总操作数 ≈ \( \frac{n(n+1)}{2} = \frac{1}{2}n^2 + \frac{1}{2}n \)
# 忽略低阶项和常数 → \( O(n^2) \)
#
# 🔹 第 4 步：处理递归函数（使用递推式或主定理）
# 方法 A：展开递归（适用于简单情况）
# python
# def factorial(n):
# if n <= 1:
# return 1
# return n * factorial(n - 1) # T(n) = T(n-1) + O(1)
# 展开：\( T(n) = T(n-1) + c = T(n-2) + 2c = \dots = T(0) + nc \)
# → \( O(n) \)
# 方法 B：主定理（Master Theorem）—— 用于分治
# 若递归式为：
# \[
# T(n) = aT\left(\frac{n}{b}\right) + O(n^d)
# \]
# 则：
# 若 \( a < b^d \) → \( T(n) = O(n^d) \)
# 若 \( a = b^d \) → \( T(n) = O(n^d \log n) \)
# 若 \( a > b^d \) → \( T(n) = O(n^{\log_b a}) \)
#
# ✅ 例子：归并排序
# \( T(n) = 2T(n/2) + O(n) \) → \( a=2, b=2, d=1 \)
# \( a = b^d \)（因为 \( 2 = 2^1 \)）→ \( O(n \log n) \)
#
# 🔹 第 5 步：应用大 O 规则简化表达式
#
# 根据讲义第 9 页：
# “Ignore constant factors and lower-order terms”
#
# 原始表达式 简化后（Big-Oh）
# ----------- ------------------
# \( 5n^3 + 2n^2 + 100 \) \( O(n^3) \)
# \( 1000 \log n + 50 \) \( O(\log n) \)
# \( 2^n + n^{100} \) \( O(2^n) \)（指数增长最快）
# \( n \log n + n \) \( O(n \log n) \)
# 📌 记住增长阶顺序（讲义 p.11）：
# \[
# 1 < \log n < n < n\log n < n^2 < n^3 < \dots < 2^n < n!
# \]
#
# ✅ 三、常见陷阱与注意事项
# ❌ 陷阱 1：误判“看似嵌套”的循环
# python
# for i in range(n):
# for j in range(100): # 内层固定 100 次！
# do_something()
# 实际：\( n \times 100 = 100n \) → \( O(n) \)，不是 \( O(n^2) \)
# ❌ 陷阱 2：忽略内置函数的复杂度
# python
# if x in my_list: # list 的 in 是 O(n)！
# ...
# list 的 in、remove、insert(0) 都是 \( O(n) \)
# set 或 dict 的 in 是 \( O(1) \)
# ❌ 陷阱 3：字符串拼接（在循环中）
# python
# s = ""
# for i in range(n):
# s += str(i) # 每次创建新字符串 → O(n²)
# 应改用 "".join(list) → \( O(n) \)
#
# ✅ 四、快速参考表（常见代码模式）
#
# 代码模式 时间复杂度
# -------- ----------
# 单层遍历数组 \( O(n) \)
# 双重嵌套遍历 \( O(n^2) \)
# 二分查找 \( O(\log n) \)
# 快速排序（平均） \( O(n \log n) \)
# 生成所有子集 \( O(2^n) \)
# 生成全排列 \( O(n!) \)
# 树的 DFS/BFS \( O(n) \)（n=节点数）
# 图的 BFS/DFS \( O(V + E) \)（V=顶点，E=边）
#
# ✅ 五、总结：判断流程图
#
# 开始
# │
# ├─▶ 确定输入规模 n
# │
# ├─▶ 有递归？ ──是──▶ 写递推式 → 用主定理或展开
# │ │
# │ 否
# │
# ├─▶ 有循环？ ──是──▶ 数嵌套层数 + 每层次数 → 相乘
# │ │
# │ 否
# │
# ├─▶ 查看内置操作（如 in, sort, slice）的复杂度
# │
# ├─▶ 写出总操作数表达式（如 3n² + 5n + 10）
# │
# └─▶ 应用 Big-Oh 规则 → 保留最高阶项 → 得到 O(...)

# 🔢 一、排序算法（Sorting Algorithms）
#
# 算法 最好情况 平均情况 最坏情况 空间复杂度 是否稳定 是否原地
# ------ -------- -------- -------- ---------- -------- --------
# 冒泡排序 (Bubble Sort) \( O(n) \) \( O(n^2) \) \( O(n^2) \) \( O(1) \) ✅ ✅
# 选择排序 (Selection Sort) \( O(n^2) \) \( O(n^2) \) \( O(n^2) \) \( O(1) \) ❌ ✅
# 插入排序 (Insertion Sort) \( O(n) \) \( O(n^2) \) \( O(n^2) \) \( O(1) \) ✅ ✅
# 希尔排序 (Shell Sort) \( O(n \log n) \) \( O(n^{1.3}) \) \( O(n^2) \) \( O(1) \) ❌ ✅
# 归并排序 (Merge Sort) \( O(n \log n) \) \( O(n \log n) \) \( O(n \log n) \) \( O(n) \) ✅ ❌
# 快速排序 (Quick Sort) \( O(n \log n) \) \( O(n \log n) \) \( O(n^2) \) \( O(\log n) \) ❌ ✅
# 堆排序 (Heap Sort) \( O(n \log n) \) \( O(n \log n) \) \( O(n \log n) \) \( O(1) \) ❌ ✅
# 计数排序 (Counting Sort) \( O(n + k) \) \( O(n + k) \) \( O(n + k) \) \( O(k) \) ✅ ❌
# 桶排序 (Bucket Sort) \( O(n) \) \( O(n) \) \( O(n^2) \) \( O(n) \) ✅ ❌
# 基数排序 (Radix Sort) \( O(d(n + k)) \) \( O(d(n + k)) \) \( O(d(n + k)) \) \( O(n + k) \) ✅ ❌
# 📌 注：
# \( n \)：元素个数；\( k \)：值域大小；\( d \)：位数。
# 比较排序下限：任何基于比较的排序算法最坏情况至少 \( \Omega(n \log n) \)（讲义 p.14 提到“高效 vs 暴力”）。
# 非比较排序（计数/桶/基数）可突破此限制，但有数据范围要求。
#
# 🔍 二、搜索算法（Searching Algorithms）
#
# 算法 数据结构 时间复杂度（平均/最坏） 备注
# ------ -------- ---------------------- ------
# 线性搜索 (Linear Search) 无序数组 \( O(n) \) 最坏需遍历全部
# 二分搜索 (Binary Search) 有序数组 \( O(\log n) \) 讲义 p.25–26 重点讲解
# 哈希表查找 Hash Table \( O(1) \) / \( O(n) \) 平均 \( O(1) \)，最坏冲突多时 \( O(n) \)
# 二叉搜索树查找 BST \( O(\log n) \) / \( O(n) \) 平衡时 \( O(\log n) \)，退化成链表时 \( O(n) \)
# 平衡 BST 查找（如 AVL, Red-Black） 平衡树 \( O(\log n) \) 保证最坏 \( O(\log n) \)
#
# 🌳 三、图算法（Graph Algorithms）
#
# 设图有 \( V \) 个顶点，\( E \) 条边。
#
# 算法 问题 时间复杂度 数据结构依赖
# ------ ------ ---------- ------------
# BFS（广度优先搜索） 最短路径（无权图） \( O(V + E) \) 邻接表
# DFS（深度优先搜索） 连通性、拓扑排序 \( O(V + E) \) 邻接表
# Dijkstra 单源最短路径（非负权） \( O((V + E) \log V) \) 优先队列（堆）
# Bellman-Ford 单源最短路径（可负权） \( O(VE) \) —
# Floyd-Warshall 所有对最短路径 \( O(V^3) \) 邻接矩阵
# Kruskal 最小生成树 \( O(E \log E) \) 并查集
# Prim 最小生成树 \( O(E \log V) \) 优先队列
#
# 🧮 四、其他经典算法
#
# 算法/操作 时间复杂度 说明
# ---------- ---------- ------
# 字符串匹配（朴素） \( O(nm) \) \( n \)=文本长，\( m \)=模式长
# KMP 算法 \( O(n + m) \) 利用前缀函数避免回溯
# 快速幂（计算 \( x^n \)） \( O(\log n) \) 讲义 p.28 练习题
# 欧几里得算法（GCD） \( O(\log \min(a,b)) \) 辗转相除
# 动态规划（一般） \( O(n^k) \) \( k \) 为状态维度（如背包 \( O(nW) \)）
# 递归斐波那契（朴素） \( O(2^n) \) 指数爆炸（讲义 p.20 提到指数级不可行）
# 记忆化斐波那契 \( O(n) \) 用空间换时间
#
# 📊 五、数据结构操作的时间复杂度
# 数组（Array）
# 操作 时间复杂度
# ------ ----------
# 索引访问 arr[i] \( O(1) \)
# 查找（无序） \( O(n) \)
# 插入/删除（末尾） \( O(1) \)（摊还）
# 插入/删除（开头/中间） \( O(n) \)
# 链表（Linked List）
# 操作 时间复杂度
# ------ ----------
# 访问第 i 个元素 \( O(n) \)
# 在已知节点后插入 \( O(1) \)
# 删除已知节点 \( O(1) \)
# 查找 \( O(n) \)
# 哈希表（Hash Table / dict）
# 操作 平均 最坏
# ------ ------ ------
# 插入、删除、查找 \( O(1) \) \( O(n) \)
# 二叉堆（Binary Heap）
# 操作 时间复杂度
# ------ ----------
# 插入 \( O(\log n) \)
# 取最大/最小值 \( O(1) \)
# 删除最大/最小值 \( O(\log n) \)
#
# ⚠️ 六、重要概念回顾（来自 Lecture 8）
#
# 1. 多项式时间 vs 指数时间（讲义 p.17）
# 高效算法：\( O(n^k) \)（k 为常数）
# 低效算法：\( O(2^n), O(n!) \) → “即使宇宙毁灭也算不完”
#
# 2. 增长阶顺序（讲义 p.11）
# \[
# O(1) < O(\log n) < O(n) < O(n \log n) < O(n^2) < O(n^3) < \cdots < O(2^n) < O(n!)
# \]
#
# 3. 大 O 忽略常数和低阶项（讲义 p.9）
# \( 5n^2 + 3n + 100 = O(n^2) \)
