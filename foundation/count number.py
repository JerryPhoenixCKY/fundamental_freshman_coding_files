import re

integers=input('give some num:')
integer=re.split(r'[,\s;:.=/]+',integers)
dic=dict()

for i in integer:
    if i not in dic:
        dic[i]=0

    dic[i]+=1
for key, value in sorted(dic.items()):
    print(f'{key} occurs {dic[key]} times')
