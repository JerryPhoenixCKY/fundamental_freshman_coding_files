import math
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))


def get_larger_prime(n):

    for i in range(int(math.sqrt(n)), 1, -1):
        if n % i == 0:
            smaller_prime = i
            larger_prime = n // i  # 整除
            return larger_prime
    return None

n = int(input())
result = get_larger_prime(n)
print(result)



# def isprime(n):
#     if n < 2:
#         return False
#     if n == 2:
#         return True  # 2 是唯一的偶数质数
#     if n % 2 == 0:
#         return False # 除了 2 以外的偶数都不是质数
#
#     return all(n % i != 0 for i in range(3, int(math.sqrt(n)) + 1, 2))
#
# def get_zhiyinshu(n):
#     for i in range(n,int(math.sqrt(n))+1,-1):
#         if n%i==0:
#             if isprime(i) and isprime(n//i):
#                 return i
#
# n=int(input())
# print(get_zhiyinshu(n))