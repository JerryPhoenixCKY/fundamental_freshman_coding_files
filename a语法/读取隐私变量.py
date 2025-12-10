# class MyClass:
#     def __init__(self):
#         self.__private = "I'm private!"
#
# obj = MyClass()
# 
# 直接访问会报错 ❌
# print(obj.__private)  # AttributeError!
#
# # 但可以通过改写后的名字访问 ✅
# print(obj._MyClass__private)  # 输出: I'm private!