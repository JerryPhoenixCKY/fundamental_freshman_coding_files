num=int(input())
lst=input().split()
s=0
for i in range(0,num):
    for j in range(0,i):
        if int(lst[j])<int(lst[i]) :
            s+=1

    print(s,end=' ')
    s=0