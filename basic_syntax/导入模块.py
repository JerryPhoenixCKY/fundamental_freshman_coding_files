#在 同一文件夹 下调用另一个 .py 文件的函数，只需：

# 方式1（推荐）
# import other_file
# other_file.function_name()
#
# # 方式2（常用）
# from other_file import function_name
# function_name()



#在不同文件夹下调用另一个 .py 文件的函数，只需：

#使用 相对导入（需包结构） —— 推荐用于项目内部模块
# 步骤 1：将目录变成 Python 包（Package）
# 在 utils/ 文件夹中创建一个空文件 __init__.py：
#

# my_project/
# │
# ├── main.py
# │
# └── utils/
#     ├── __init__.py   ← 新增这个文件（可以为空）
#     └── sorting.py

# 💡 __init__.py 的存在告诉 Python：utils 是一个可导入的包。

#
# 步骤 2：在 main.py 中导入

# # main.py
#
# # 方法 A：直接导入模块
# from utils import sorting
#
# result = sorting.quicksort([3, 1, 4])
#
# # 方法 B：导入具体函数
# from utils.sorting import quicksort
#
# result = quicksort([3, 1, 4])
# ✅ 这是最标准、最推荐的方式，尤其适合组织大型项目。
#
# ✅ 方法二：修改 sys.path（临时添加路径）—— 简单但不优雅
# 如果你不想创建 __init__.py，或者文件在完全不同的地方，可以用 sys.path 手动添加路径：
# # main.py
# import sys
# import os
#
# # 获取当前脚本所在目录
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 构造 utils 的绝对路径
# utils_path = os.path.join(current_dir, 'utils')
#
# # 将 utils 目录加入 Python 模块搜索路径
# sys.path.append(utils_path)
#
# # 现在可以直接导入 sorting.py（因为 Python 把它当顶层模块）
# import sorting
#
# result = sorting.quicksort([5, 2, 8])