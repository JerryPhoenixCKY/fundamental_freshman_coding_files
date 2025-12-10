class Fruit:
    pass

class Apple(Fruit):
    def make_cider(self):
        return "Apple cider made!"

class Orange(Fruit):
    def make_juice(self):
        return "Orange juice made!"

class GoldenDelicious(Apple):
    pass

golden = GoldenDelicious()
orange = Orange()

print(isinstance(golden, Fruit))        # True
print(isinstance(golden, Apple))        # True
print(isinstance(golden, GoldenDelicious))  # True
print(isinstance(orange, Apple))        # False

# 安全调用方法
if isinstance(golden, Apple):
    print(golden.make_cider())  # 可以调用


