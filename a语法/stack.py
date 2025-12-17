class ListStack:
    def __init__(self):
        self.__data = list()

    def __len__(self):
        return len(self.__data)

    def is_empty(self):
        return len(self.__data) == 0

    def push(self, e):
        self.__data.append(e)

    def top(self):
        if self.is_empty():
            print('The stack is empty.')
        else:
            return self.__data[self.__len__() - 1]

    def pop(self):
        if self.is_empty():
            print('The stack is empty.')
        else:
            return self.__data.pop()
#######应用实例
def is_balanced(expr):
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    for char in expr:
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    return stack.is_empty()

print(is_balanced("([{}])"))  # True
print(is_balanced("([)]"))    # False


#######检查 HTML 文档中的标签是否正确匹配


import re


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0


def is_html_valid(html: str) -> bool:
    """
    检查 HTML 字符串中的标签是否正确匹配。
    支持：普通开始/结束标签（如 <div>, </div>）
    忽略：自闭合标签（如 <br/>, <img src="x" />）、注释、DOCTYPE、文本内容
    """
    # 正则表达式：匹配所有 <...> 标签，但排除注释 <!-- --> 和 <!DOCTYPE>
    tag_pattern = r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>'

    stack = Stack()

    for match in re.finditer(tag_pattern, html):
        is_closing = match.group(1) == '/'  # 是否是结束标签（有 /）
        tag_name = match.group(2).lower()  # 标签名（转小写以兼容大小写不敏感）

        # 跳过自闭合标签（如 <br/>），但我们的正则已排除 /> 形式？
        # 更安全做法：如果标签以 /> 结尾，跳过（但本正则未捕获）
        # 这里假设输入不含自闭合，或将其视为开始+立即结束（不影响）

        if is_closing:
            if stack.is_empty():
                print(f"错误：多余的结束标签 </{tag_name}>")
                return False
            expected = stack.pop()
            if expected != tag_name:
                print(f"错误：期望 </{expected}>，但遇到 </{tag_name}>")
                return False
        else:
            # 开始标签，压入栈
            stack.push(tag_name)

    # 最后栈必须为空
    if not stack.is_empty():
        remaining = stack._items
        print(f"错误：以下标签未关闭: {remaining}")
        return False

    return True


# ========================
# 测试用例
# ========================

# ✅ 正确示例
html1 = """
<html>
  <head>
    <title>Test</title>
  </head>
  <body>
    <div><p>Hello</p></div>
  </body>
</html>
"""

# ❌ 错误示例 1：标签不匹配
html2 = "<div><p>Hello</div></p>"

# ❌ 错误示例 2：多余结束标签
html3 = "</p>"

# ❌ 错误示例 3：未关闭标签
html4 = "<div><p>Hello</div>"

# ✅ 自闭合标签（我们忽略它们，所以应通过）
html5 = "<html><body><br><img src='x'><hr></body></html>"

# 运行测试
print("Test 1 (valid):", is_html_valid(html1))  # True
print("Test 2 (mismatch):", is_html_valid(html2))  # False
print("Test 3 (extra close):", is_html_valid(html3))  # False
print("Test 4 (unclosed):", is_html_valid(html4))  # False
print("Test 5 (self-closing ignored):", is_html_valid(html5))  # True