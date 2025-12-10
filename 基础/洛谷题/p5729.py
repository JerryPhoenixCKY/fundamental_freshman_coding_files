# 读取立方体尺寸
w, x, h = map(int, input().split())

# 创建一个三维布尔数组，表示每个小方块是否还存在
# True 表示存在，False 表示已被切掉
cube = [[[True for _ in range(h+1)] for _ in range(x+1)] for _ in range(w+1)]

# 读取切割次数
q = int(input())

# 执行 q 次切割
for _ in range(q):
    x1, y1, z1, x2, y2, z2 = map(int, input().split())
    # 遍历被切掉的区域，标记为 False
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            for k in range(z1, z2 + 1):
                cube[i][j][k] = False

# 统计剩余的小方块数量
count = 0
for i in range(1, w + 1):
    for j in range(1, x + 1):
        for k in range(1, h + 1):
            if cube[i][j][k]:
                count += 1

print(count)

# cube=input().split()
# group=[]
# x=int(cube[0])
# y=int(cube[1])
# z=int(cube[2])
# for i in range(1,x+1):
#     for j in range(1, y+ 1):
#         for k in range(1, z + 1):
#             group.append([i,j,k])
#
# times=int(input())
# for t in range(times):
#     cut=input().split()
#     x1=int(cut[0])
#     y1=int(cut[1])
#     z1=int(cut[2])
#     x2=int(cut[3])
#     y2=int(cut[4])
#     z2=int(cut[5])
#     for i in range(x1, x2+1):
#         for j in range(y1, y2+1):
#             for k in range(z1, z2+1):
#                 group= [x for x in group if x !=[i,j,k]]
#
# c=len(group)
# print(c)
