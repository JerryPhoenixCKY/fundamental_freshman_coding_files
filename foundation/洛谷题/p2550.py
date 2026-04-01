times=int(input())
ans=set(map(int,input().split()))
output=[0]*7
for t in range(times):
    count=0
    num=map(int,input().split())
    for i in num:
        if i in ans:
            count+=1
    if count>0:
        output[-count]+=1
print(*output)