# 读入一行，分割成整数列表
s = list(map(int, input().split()))
n = len(s)
total_sum = sum(s)

# 所有子集元素之和 = 总和 * 2^(n-1)
result = total_sum * (2 ** (n - 1))

print(result)