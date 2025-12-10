n= int(input()) # 输入n，类型为整数
a = [[0 for i in range(0, n+1)] for j in range(0, n)] # 建立数组
a[0][1] =1 # 标记a[1][1]的值为1
for i in range(1, n): # range(a,b)表示在[a,b)区间，不包括b
    for j in range(1, i+2):
        a[i][j] = a[i-1][j-1] + a[i-1][j] # 递推
for i in range(0, n):
    for j in range(1, i+2):
        print(a[i][j], end = ' ') # end=''可以在输出内容后多输出一个字符串，不写end则默认为换行
    print('') # 输出空，因为默认输出后换行，所以达到了换行作用
n = int(input()) # 输入n，类型为整数

