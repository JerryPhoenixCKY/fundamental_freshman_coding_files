n = int(input())
magic_square = [[0] * n for _ in range(n)]
# 起始位置：第一行中间
row, col = 0, n // 2
magic_square[row][col] = 1
# 从 2 到 n*n 依次填入数字
for num in range(2, n * n + 1):
    # 下一步尝试移动：右上方向 (row-1, col+1)
    new_row = row - 1
    new_col = col + 1

    # 边界检查 + 是否已填过
    if new_row < 0:
        new_row = n - 1  # 越上界 → 回到最后一行
    if new_col >= n:
        new_col = 0      # 越右界 → 回到第一列

    # 如果新位置已被填，则改为正下方
    if magic_square[new_row][new_col] != 0:
        new_row = row + 1  # 正下方
        new_col = col      # 同列

    # 填入当前数字
    magic_square[new_row][new_col] = num
    row, col = new_row, new_col

# 输出结果
for i in range(n):
    print(' '.join(map(str, magic_square[i])))