lst=[88,89,90,98,0,99]
print(lst)

'''
for i in range(len(lst)):
    if str(lst[i]) == "0":
        lst[i]='200'+str(lst[i])
    else:
        lst[i]='19'+str(lst[i])
print(lst)
'''
for i,v in enumerate(lst):
    if str(lst[i]) == "0":
        lst[i]='200'+str(v)
    else:
        lst[i]='19'+str(v)
print(lst)