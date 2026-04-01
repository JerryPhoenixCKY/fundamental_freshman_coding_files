
lst=['1001手机','1002水杯','1003电脑','1004猫粮','1005键盘','1006外套']
print('商品列表如下',lst)
cart=[]
while True:
    flag=False
    num=input('输入要购买的商品编号：')
    for i in lst:
        if num==i[:4]:
            flag=True
            cart.append(i)
            print('成功添加商品')
            break
    if not flag and num!='q':
        print('商品不存在')
    if num=='q':
        break
print('-'*50)
cart.reverse()
print('您购物车里的商品如下：')
for i in cart:
    print(i)
