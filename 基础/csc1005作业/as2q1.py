import math

def reverse_integer(x):
    return int(str(x)[::-1])

def isprime(x):
    in_count=0
    if x%2 == 0:
        return False
    for i in range(3,math.isqrt(x),2):
        if x%i==0:
            return False
    return True

def issquare(n):
    if n < 0:
        return False
    r= math.isqrt(n)
    return r*r==n

num = int(input())
count = 0
reversible = 16

while count < num:
    if issquare(reversible):
        turn = reverse_integer(reversible)
        if isprime(turn):
            print(reversible, end=' ')
            count += 1
            if count % 10 == 0:
                print()
    reversible += 1
if count % 10 != 0:
    print()