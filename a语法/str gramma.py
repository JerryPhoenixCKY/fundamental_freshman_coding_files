s1='HELLOworld'
s2=s1.lower()
print(s2)
s3=s1.upper()
print(s3)

########################################################################

em='qwertyu@qq.com'
lst=em.split('@',-1)
print('邮件名：',lst[0],'邮件服务器名',lst[1])

# 多个不同分隔符一次分隔
import re

text = "a, b; c\td\ne"  # 包含逗号、空格、分号、制表符、换行
result = re.split(r'[,\s;]+', text)  # \s 表示任意空白字符
print(result)
# 输出: ['a', 'b', 'c', 'd', 'e']


"""再看一遍

import re

def multi_split(text, delimiters):
    # 构建正则表达式：把分隔符放入 []
    pattern = '[' + re.escape(''.join(delimiters)) + ']'
    return [part for part in re.split(pattern, text) if part]

# 使用
text = "a,b;c|d"
print(multi_split(text, [',', ';', '|']))  # ['a', 'b', 'c', 'd']
"""

#######################################################################

print(s1.count('o'),
s1.find('o'),
s1.index('o'),
s1.index('r'),
s1.startswith('H'),
s1.replace('L','D',1),
s1.center(15,'#'),)
#去除字符串左右空格strip rstrip，lstrip，去除特定字符串（没有顺序，有就都删）
s2=s1.strip()

#######################################################################

x='calculus'
y='潘潘'
print(x+y)


line='hellopython'
if line.startswith('hello'):
    print("yes")

import re

def multi_split(text, delimiters):
    # 构建正则表达式：把分隔符放入 []
    pattern = '[' + re.escape(''.join(delimiters)) + ']'
    return [part for part in re.split(pattern, text) if part]

# 使用
text = "a,b;c|d"
print(multi_split(text, [',', ';', '|']))
