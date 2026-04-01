class student():
    def __init__(self,name,age,gender):
        self._name=name #受保护，只能本类子类访问
        self.__age=age#私有的，只有本身能访问


class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

t = Temperature(25)
print(t.celsius)      # 25
t.celsius = 30        # ✅ 合法
# t.celsius = -300    # ❌ 抛出异常


class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # “受保护”，建议不要直接访问

    def deposit(self, amount):
        self._balance += amount

acc = BankAccount(100)
print(acc._balance)  # ⚠️ 技术上可行，但违反约定

class MyClass:
    def __init__(self):
        self.__private = 42  # 实际存储为 _MyClass__private

obj = MyClass()
# print(obj.__private)        # ❌ AttributeError
print(obj._MyClass__private)  # ✅ 42（仍可访问，但不推荐



class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """获取摄氏度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏度（带验证）"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度！")
        self._celsius = value

    @property
    def fahrenheit(self):
        """只读：摄氏转华氏"""
        return self._celsius * 9 / 5 + 32

t = Temperature(25)
print(t.celsius)      # 25
print(t.fahrenheit)   # 77.0

t.celsius = 30        # ✅ 触发 setter
# t.celsius = -300    # ❌ 抛出 ValueError