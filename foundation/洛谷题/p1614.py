m,n=map(int,input().split())
all_num=[]
for i in range(m):
    num=int(input())
    all_num.append(num)
sum1=0
for i in range(n):
    sum1+=all_num[i]

sum_lst=[sum1]
for i in range(n,m):
    sum1+=all_num[i]-all_num[i-n]
    sum_lst.append(sum1)

result=min(sum_lst)
print(result)

