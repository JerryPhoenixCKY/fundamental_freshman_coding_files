# 输入 n, m, k
n, m, k = map(int, input().split())

# 初始化棋盘：True 表示“暗”（会出怪），False 表示“光”（被照亮）
grid = [[True] * n for _ in range(n)]

# 处理火把：照亮 3x3 区域
for _ in range(m):
    x, y = map(int, input().split())
    # 将坐标转换为 0-based（Python索引从0开始）
    x -= 1
    y -= 1
    # 遍历以 (x,y) 为中心的 3x3 区域
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            # 检查是否在棋盘范围内
            if 0 <= nx < n and 0 <= ny < n:
                grid[nx][ny] = False  # 标记为“光”
    if 0<=x-2<n and 0<=y-2<n:
        grid[x-2][y-2] = False
    if 0<=x+2<n and 0<=y-2<n:
        grid[x+2][y-2] = False
    if 0<=x-2<n and 0<=y+2<n:
        grid[x-2][y+2] = False
    if 0<=x+2<n and 0<=y+2<n:
        grid[x+2][y+2] = False



# 处理萤石：照亮 5列（y方向）× 5行（x方向）区域
for _ in range(k):
    o, p = map(int, input().split())
    o -= 1  # 转换为0-based
    p -= 1

    for dx in [-2, -1, 0, 1, 2]:  # x方向偏移
        for dy in [-2,-1, 0, 1,2]:     # y方向偏移
            nx, ny = o + dx, p + dy
            if 0 <= nx < n and 0 <= ny < n:
                grid[nx][ny] = False

# 统计未被照亮的格子数（即“暗”的点，会出怪物）
count = 0
for i in range(n):
    for j in range(n):
        if grid[i][j]:
            count += 1

print(count)



# n,m,k=map(int,input().split())
# square=[[True for i in range(n)] for i in range(n)]
#
# for _ in range(m):
#     x1,y1=map(int,input().split())
#     square[x1-1][y1-1]=False
#     square[x1 - 1][y1-2] = False
#     square[x1 - 1][y1-3] = False
#     square[x1 - 1][y1] = False
#     square[x1-1][y1+1] = False
#     square[x1-2][y1-1] = False
#     square[x1-3][y1-1] = False
#     square[x1][y1-1] = False
#     square[x1+1][y1 - 1] = False
#     square[x1 - 2][y1 - 2] = False
#     square[x1 - 2][y1] = False
#     square[x1][y1] = False
#     square[x1][y1 - 2] = False
#
# for _ in range(k):
#     x2,y2=map(int,input().split())
#     square[x2-1][y2-3]=False
#     square[x2-1][y2-2] = False
#     square[x2-1][y2-1] = False
#     square[x2-1][y2] = False
#     square[x2-1][y2+1] = False
#
#     square[x2 - 2][y2 - 3] = False
#     square[x2 - 2][y2 - 2] = False
#     square[x2 - 2][y2 - 1] = False
#     square[x2 - 2][y2] = False
#     square[x2 - 2][y2 + 1] = False
#
#     square[x2 - 3][y2 - 3] = False
#     square[x2 - 3][y2 - 2] = False
#     square[x2 - 3][y2 - 1] = False
#     square[x2 - 3][y2] = False
#     square[x2 - 3][y2 + 1] = False
#
#     square[x2][y2 - 3] = False
#     square[x2][y2 - 2] = False
#     square[x2][y2 - 1] = False
#     square[x2][y2] = False
#     square[x2][y2 + 1] = False
#     square[x2+1][y2 - 3] = False
#     square[x2 +1][y2 - 2] = False
#     square[x2+1][y2 - 1] = False
#     square[x2+1][y2] = False
#     square[x2+1][y2 + 1] = False
#     square[x2 +2][y2 - 3] = False
#     square[x2+2][y2 - 2] = False
#     square[x2 +2][y2 - 1] = False
#     square[x2+2][y2] = False
#     square[x2 +2][y2 + 1] = False
#
# count=0
# for i in range(n):
#     for j in range(n):
#         if square[i][j]:
#             count+=1
#
#
# print( count)