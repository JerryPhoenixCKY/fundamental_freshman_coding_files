import copy
a=[1,2,[3,4]]
b=a
c=copy.copy(a)
d=a[:]
e=copy.deepcopy(a)
print(a,b,c,d,e,sep='\n')
a.append(5)
print(a,b,c,d,e,sep='\n')
a[2][0]=6
print(a,b,c,d,e,sep='\n')