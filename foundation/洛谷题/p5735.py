# # P5735 【深基7.例1】距离函数
# ## 题目描述
# 给出平面坐标上不在一条直线上三个点坐标 $(x_1,y_1),(x_2,y_2),(x_3,y_3)$，坐标值是实数，且绝对值不超过 100.00，求围成的三角形周长。保留两位小数。
# 对于平面上的两个点 $(x_1,y_1),(x_2,y_2)$，则这两个点之间的距离 $dis=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$。
# ## 输入格式
# 输入三行，第 $i$ 行表示坐标 $(x_i,y_i)$，以一个空格隔开。
# ## 输出格式
# 输出一个两位小数，表示由这三个坐标围成的三角形的周长。
# # 说明/提示
# 数据保证，坐标均为实数且绝对值不超过 $100$，小数点后最多仅有 $3$ 位。
import math
point=[(a,b) for a,b in [map(float,input().split()) for _ in range(3)]]
def dis(p1,p2):
    return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
final=dis(point[0],point[1])+dis(point[1],point[2])+dis(point[2],point[0])
final = round(final, 2)
print(final)