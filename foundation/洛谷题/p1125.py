import math

def is_prime(n):
    """判断 n 是否为质数"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # 从 3 到 sqrt(n)，步长为 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True
# 读取输入
word = input().strip()
# 统计每个字母出现次数
freq = {}
for char in word:
    freq[char] = freq.get(char, 0) + 1
# 找最大和最小频率
max_freq = max(freq.values())
min_freq = min(freq.values())
diff = max_freq - min_freq
# 判断是否为 Lucky Word
if diff < 2 or not is_prime(diff):
    print("No Answer")
    print(0)
else:
    print("Lucky Word")
    print(diff)




# import math
# def isprime(x):
#     if x<2:
#         return False
#     if x%2 == 0:
#         return False
#     for i in range(3,math.isqrt(x)+1,2):
#         if x%i==0:
#             return False
#     return True
# str_in=input().split()
# count={}
# for char in str_in:
#     count[char] = count.get(char, 0) + 1
#
# maxnum=max(count.values())
# minnum=min(count.values())
# if maxnum-minnum<=1:
#     print('No Answer')
#     print(0)
# elif isprime(maxnum-minnum):
#     print('Lucky Word')
#     print(maxnum-minnum)
# else:
#     print('No Answer')
#     print(0)

