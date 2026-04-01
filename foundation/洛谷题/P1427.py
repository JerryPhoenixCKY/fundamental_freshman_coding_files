lst=input().split()
del lst[-1]
lst=lst[::-1]
for i in lst:
    print(i,end=' ')