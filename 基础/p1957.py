n = int(input())
op = None

for _ in range(n):
    line = input().strip()

    if line[0].isalpha():
        op = line[0]
        a, b = map(int, line[2:].split())
    else:
        a, b = map(int, line.split())

    if op == 'a':
        res = a + b
        expr = f"{a}+{b}={res}"
    elif op == 'b':
        res = a - b
        expr = f"{a}-{b}={res}"
    elif op == 'c':
        res = a * b
        expr = f"{a}*{b}={res}"

    print(expr)
    print(len(expr))

# def yunsuan(line,count):
#     line_lst=line.split()
#     s=line_lst.pop(0)
#     if s=='a':
#         A=int(line_lst[0])+int(line_lst[1])
#         return line_lst[0]+'+'+line_lst[1]+'='+str(A)+'\n'+str(len(line)-1+len(str(A)))
#     elif s=='b':
#         B=int(line_lst[0])-int(line_lst[1])
#         return line_lst[0]+'-'+line_lst[1]+'='+str(B)+'\n'+str(len(line)-1+len(str(B)))
#     elif s=='c':
#         C=int(line_lst[0])*int(line_lst[1])
#         return line_lst[0]+'*'+line_lst[1]+'='+str(C)+'\n'+str(len(line)-1+len(str(C)))
#
#
# n=int(input())
# count=[]  # 将count移到循环外部，使其能够在迭代之间保持状态
# for i in range(n):
#     line=input()
#     if line[0].isalpha():
#         count.append(line[0]+' ')
#         print(yunsuan(line,count))
#     else:
#         line=count.pop()+line
#         print(yunsuan(line,count))

