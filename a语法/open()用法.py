"""
模式	   用途      是否清空	    是否创建
'r'	  读文本	       否	     否（不存在报错）
'w'	  写文本 	✅ 是	     ✅ 是
'a'	  追加文本	   否	     ✅ 是
'rb'  读二进制	   否	     否
'wb'  写二进制	✅ 是	     ✅ 是
'r+'  读写文本	   否	     否
'w+'  读写文本	✅ 是	     ✅ 是
"""

# open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)


# 方式1：使用 with（自动关闭文件，强烈推荐！）
with open("example.txt", "r", encoding="utf-8") as f:
    content = f.read()        # 读取全部内容
    # 或
    lines = f.readlines()     # 读取所有行（返回列表）
    # 或
    for line in f:            # 逐行读取（节省内存）
        print(line.strip())

# 覆盖写入
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("第二行\n")

# 追加内容
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新日志\n")

# 复制图片
with open("photo.jpg", "rb") as src:
    with open("photo_copy.jpg", "wb") as dst:
        dst.write(src.read())


# 如不用with,要用close（）关闭文件


# 使用try except 防止报错
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("文件不存在！")
except UnicodeDecodeError:
    print("编码错误，请检查 encoding 参数")