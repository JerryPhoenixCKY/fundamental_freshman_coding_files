n=int(input())
lst=input().split()
lst_final=[]
for i in range(n):
    for j in range(i+1, n):
        s=int(lst[i])+ int(lst[j])
        if str(s) in lst and s not in lst_final:
            lst_final.append(s)

print(len(lst_final))
