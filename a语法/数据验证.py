"""

1. 字符串内容验证
方法	作用	示例
str.isdigit()	是否全为数字（正整数）	'123'.isdigit() → True
str.isnumeric()	是否为数字（包括中文(大写）数字、罗马数字、Unicode 数字）	'①'.isnumeric() → True
str.isdecimal()	是否为十进制数字（最严格）	'123'.isdecimal() → True
str.isalpha()	是否全为字母	'abc'.isalpha() → True
str.isalnum()	是否为字母或数字（包含中文字符）	'a1b2'.isalnum() → True
str.isspace()	是否为空白字符	' \t\n'.isspace() → True
str.islower() / isupper()	是否全小写/大写	'HELLO'.isupper() → True
str.istitle()     所有字符都是首字母大写
str.isspace()      所有字符都是空白字符（\n）（\t）
⚠️ 注意：这些方法对空字符串返回 False。

2. 类型检查
方法	说明
type(x) is int	严格类型检查（不推荐用于继承）
isinstance(x, int)	推荐！支持继承（如 bool 是 int 的子类）
isinstance(x, (int, float))	检查是否为多个类型之一


isinstance(42, int)        # True
isinstance(True, int)      # True（因为 bool 是 int 子类）
isinstance("123", str)     # True
"""
print('cat我'.isalpha())
print('123'.isdigit())
print('123'.isalpha())
print('123'.isnumeric())
print('year'.isalpha())
print('壹贰叁'.isnumeric())
print("Alpha".istitle())
print('\n'.isspace() ,'\t'.isspace() ,' '.isspace() )
