# 父类
class GeometricObject:
    def __init__(self, color="white", filled=False):
        self.color = color
        self.filled = filled

    def __str__(self):
        return f"Color: {self.color}, Filled: {self.filled}"

# 子类 1
class Circle(GeometricObject):
    def __init__(self, radius=1.0, color="white", filled=False):
        super().__init__(color, filled)  # 调用父类构造器
        self.radius = radius

    def get_area(self):
        return 3.14159 * self.radius ** 2

    def __str__(self):
        return f"Circle: radius={self.radius}, " + super().__str__()

# 子类 2
class Rectangle(GeometricObject):
    def __init__(self, width=1.0, height=1.0, color="white", filled=False):
        super().__init__(color, filled)
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

    def __str__(self):
        return f"Rectangle: width={self.width}, height={self.height}, " + super().__str__()

def display_area(obj):
    print(f"Area: {obj.get_area()}")  # 动态绑定：自动调用 Circle 或 Rectangle 的 get_area

c = Circle(2.0, "red", True)
r = Rectangle(3.0, 4.0, "blue", False)

display_area(c)  # 输出: Area: 12.56636
display_area(r)  # 输出: Area: 12.0
