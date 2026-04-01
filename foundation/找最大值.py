import random

def get_max(lst):
    x=lst[0]
    for i in range(1,len(lst)):
        if lst[i]>x:
            x=lst[i]
    return x
lst=[random.randint(1,100) for i in range(10)]
print(lst)
max=get_max(lst)
print(max)
