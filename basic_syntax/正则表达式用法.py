
"""
re.compile(pattern, flags=0)	编译正则表达式，返回一个 Pattern 对象（可复用）
re.match(pattern, string, flags=0)	从字符串开头匹配，只匹配一次
re.search(pattern, string, flags=0)	在整个字符串中搜索第一个匹配项
re.findall(pattern, string, flags=0)	返回所有非重叠匹配的列表
re.finditer(pattern, string, flags=0)	返回一个迭代器，包含所有匹配的 Match 对象
re.sub(pattern, repl, string, count=0, flags=0)	替换匹配项
re.subn(pattern, repl, string, count=0, flags=0)	替换并返回（新字符串, 替换次数）元组
re.split(pattern, string, maxsplit=0, flags=0)	按匹配项分割字符串

"""

import re
# match示例
# 只作用在开头
pattern=r'\d\.\d+'#要加r，非常重要
s='okokokokokokokok3.1212121212112212121'
match=re.match(pattern,s,re.IGNORECASE)
print(match)


s2='3.1212121212112212121okokokokokokokok'
match2=re.match(pattern,s2)
print(match2)#<re.Match object; span=(0, 21), match='3.1212121212112212121'>

print(match2.start(),match2.end(),match2.span(),'待匹配的数据',match2.string,'匹配的数据',match2.group(),sep='\n',end='')

print("\n")

#search示例

pattern=r'\d\.\d+'#要加r，非常重要
s3='it is a string1.345'
match3=re.search(pattern,s3)
print(match3)
print(match3.group())

# findall示例
# 注意输出的是列表
s4='3.14it is a string1.345'
match4=re.findall(pattern,s4)
print(match4)

# sub示例
pattern2='黑客|破解|反爬'
s5='我想学习Python，想破解一些VIP视频，Python可以实现无底线反爬吗？'
match5=re.sub(pattern2,'xxx',s5)
print(match5)



#split示例  输出是列表  会把分隔符去掉
s6='https://zh.hail101.ru/book/6070294counselling-for-toads-a-psychological-adventure.html?dsource=mostpopular'
pattern3='[/-]'
match6=re.split(pattern3,s6)
print(match6)




# 1. 编译一个正则表达式模式，用于匹配连续的数字
pattern = re.compile(r'\d+')

# 2. 使用编译后的 Pattern 对象进行匹配
text1 = "There are 123 apples and 456 oranges."
text2 = "The price is 789 dollars."

# 在 text1 中查找所有数字
matches1 = pattern.findall(text1)
print("Matches in text1:", matches1)  # 输出: Matches in text1: ['123', '456']

# 在 text2 中查找所有数字
matches2 = pattern.findall(text2)
print("Matches in text2:", matches2)  # 输出: Matches in text2: ['789']

# 3. 使用 flags (例如，忽略大小写)
text_with_case = "Python, python, PYTHON, PyThOn"
case_insensitive_pattern = re.compile(r'python', re.IGNORECASE)
found = case_insensitive_pattern.findall(text_with_case)
print("Case-insensitive matches:", found)  # 输出: Case-insensitive matches: ['Python', 'python', 'PYTHON', 'PyThOn']

# 4. Pattern 对象的其他方法
compiled_pattern = re.compile(r'(\d+)-(\d+)-(\d+)') # 匹配日期格式 YYYY-MM-DD 并分组
date_text = "Today is 2023-10-26."
match_obj = compiled_pattern.search(date_text)

if match_obj:
    print("Full match:", match_obj.group(0))  # 输出完整匹配 '2023-10-26'
    print("Year:", match_obj.group(1))        # 输出第一组 '2023'
    print("Month:", match_obj.group(2))       # 输出第二组 '10'
    print("Day:", match_obj.group(3))         # 输出第三组 '26'
else:
    print("No date found.")
