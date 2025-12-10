# # 输入
# start, end = map(int, input().split())
#
# # 初始化统计数组：0~9 出现次数
# count = [0] * 10
#
# # 遍历每个数字
# for num in range(start, end + 1):
#     # 将数字转为字符串，逐位处理
#     for digit_char in str(num):
#         digit = int(digit_char)
#         count[digit] += 1
#
# # 输出结果
# print(' '.join(map(str, count)))

def devide(x):
    x1=str(x)
    x1=' '.join(x1)
    return x1.split()

start,end=map(int,input().split())
final=[0]*10
for i in range(start,end+1):
    lst=devide(i)
    for j in lst:
        final[int(j)]+=1

print(' '.join(map(str, final)))

