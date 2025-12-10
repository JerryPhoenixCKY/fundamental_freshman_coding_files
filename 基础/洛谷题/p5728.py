# # P5728 【深基5.例5】旗鼓相当的对手
#
# ## 题目描述
#
# 现有 $N$ 名同学参加了期末考试，并且获得了每名同学的信息：语文、数学、英语成绩（均为不超过 $150$ 的自然数）。
# 如果某对学生 $\lang i,j\rang$ 的每一科成绩的分差都不大于 $5$，且总分分差不大于 $10$，那么这对学生就是“旗鼓相当的对手”。
# 现在想知道这些同学中，有几对“旗鼓相当的对手”？同样一个人可能会和其他好几名同学结对。
# ## 输入格式
# 第一行一个正整数 $N$。
# 接下来 $N$ 行，每行三个整数，其中第 $i$ 行表示第 $i$ 名同学的语文、数学、英语成绩。最先读入的同学编号为 $1$。
# ## 输出格式
# 输出一个整数，表示“旗鼓相当的对手”的对数。

#第一版错误！！！！！！！！！！！！！错！！！！！！！！！！I'm fw ！！！！！！！！！！！！！！！！！！
# i=int(input())
# lst=[]
# for j in range(i+1):
#     a,b,c=input().split()
#     lst.append([int(a),int(b),int(c)])
# l=0
# s=[]
# for item in lst :
#     s[l]=item[0]+item[1]+item[2]
#     l+=1
# s1=[]
# for i in range(len(s)):
#     for j in range(i+1,len(s)):
#         if -10<=i-j<=10:
#             s1.append([i,j])
# count=0
# for i in s1:
#     if -5<=lst[s1[i][0]][0]-lst[s1[i][1]][0]<=5 and -5<=lst[s1[i][0]][1]-lst[s1[i][1]][1]<=5 and -5<=lst[s1[i][0]][2]-lst[s1[i][1]][2]<=5:
#         count+=1
#
#
# print(count)

n = int(input())
students = []
for _ in range(n):
    a, b, c = map(int, input().split())
    students.append([a, b, c])

count = 0
for i in range(n):
    for j in range(i + 1, n):  # j > i，避免重复
        # 检查每科成绩差是否 ≤ 5
        if (abs(students[i][0] - students[j][0]) <= 5 and
            abs(students[i][1] - students[j][1]) <= 5 and
            abs(students[i][2] - students[j][2]) <= 5):
            # 检查总分差是否 ≤ 10
            total_i = sum(students[i])
            total_j = sum(students[j])
            if abs(total_i - total_j) <= 10:
                count += 1

print(count)


# --------------------------------------------------------------
n = int(input())
scores = [list(map(int, input().split())) for _ in range(n)]

count = 0
for i in range(n):
    for j in range(i + 1, n):
        # 每科成绩差不超过5
        if (abs(scores[i][0] - scores[j][0]) <= 5 and
            abs(scores[i][1] - scores[j][1]) <= 5 and
            abs(scores[i][2] - scores[j][2]) <= 5):
            # 总分差不超过10
            if abs(sum(scores[i]) - sum(scores[j])) <= 10:
                count += 1

print(count)