mydict={'a':100,'b':10,'c':11,'d':21}
mylist=mydict.items()
print(mylist)

newlist=list()
for i in mylist:
    newtuple=(i[1],i[0])
    newlist.append(newtuple)

print(newlist)
print(sorted(newlist))