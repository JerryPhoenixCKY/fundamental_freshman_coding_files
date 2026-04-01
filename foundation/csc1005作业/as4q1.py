def HanoiTower(n):
    """
    使用栈模拟递归，解决汉诺塔问题（非递归版本）
    输入: n - 盘子数量
    输出: 打印每一步移动，如 "A --> C"
    """
    if n <= 0:
        return

    # 栈用于模拟递归调用
    # 每个元素是 (盘子数量, 源柱, 辅助柱, 目标柱)
    stack = []
    # 初始任务：将 n 个盘子从 'A' 移动到 'C'，'B' 为辅助柱
    stack.append((n, 'A', 'B', 'C'))

    while stack:
        # 出栈一个任务
        count, src, aux, dest = stack.pop()

        if count == 1:
            # 基础情况：直接移动一个盘子
            print(f"{src} -> {dest}")
        else:
            # 将递归的三个步骤逆序压栈，确保执行顺序正确

            # 步骤 3: 将 count-1 个盘子从 aux 移动到 dest (借助 src)
            # 这个任务应该最后执行，所以最先压栈
            stack.append((count - 1, aux, src, dest))

            # 步骤 2: 将第 count 个盘子从 src 移动到 dest
            # 这个任务在中间执行，次之压栈
            stack.append((1, src, aux, dest)) # 对于单个盘子移动，aux和dest的顺序不影响，但为了保持参数一致性，这里aux和dest位置应该和下面保持一致

            # 步骤 1: 将 count-1 个盘子从 src 移动到 aux (借助 dest)
            # 这个任务应该最先执行，所以最后压栈
            stack.append((count - 1, src, dest, aux))


#递归算法
# def hanoi(n, src, aux, dest):
#     if n == 1:
#         print(f"{src} -> {dest}")
#     else:
#         hanoi(n-1, src, dest, aux)   # 1. 把上面 n-1 个移到辅助柱
#         print(f"{src} -> {dest}")     # 2. 移动最大的盘子
#         hanoi(n-1, aux, src, dest)   # 3. 把 n-1 个从辅助柱移到目标柱