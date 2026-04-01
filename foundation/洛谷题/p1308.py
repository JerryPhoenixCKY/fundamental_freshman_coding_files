# 极快版
def main():
    word = input().strip().lower()
    text = input()

    # 转换为小写并分割
    words = text.lower().split()

    # 统计出现次数
    count = words.count(word)#####！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

    if count == 0:
        print(-1)
    else:
        # 找到第一次出现的位置
        # 在原始文本中查找（考虑单词边界）
        first_pos = text.lower().find(' ' + word + ' ')##########！！！！！！！！！！！！！！！！

        if first_pos == -1:
            # 可能在开头
            if text.lower().startswith(word + ' '):
                first_pos = 0
            # 可能在结尾
            elif text.lower().endswith(' ' + word):
                first_pos = len(text) - len(word)
        else:
            first_pos += 1  # 跳过前面的空格

        print(f"{count} {first_pos}")


if __name__ == "__main__":
    main()






pattern = input().strip().lower()
article = input()

n = len(article)
i = 0
count = 0
first_pos = -1

while i < n:
    # 跳过空格
    while i < n and article[i] == ' ':
        i += 1

    if i >= n:
        break

    # 记录单词起始位置
    start = i
    # 提取整个单词（不转存，直接比较）
    while i < n and article[i] != ' ':
        i += 1

    # 直接切片并转小写比较（避免存储）
    if article[start:i].lower() == pattern:
        count += 1
        if first_pos == -1:
            first_pos = start

print(f"{count} {first_pos}" if count else -1)




# pattern = input().strip().lower()      # 目标单词，转小写
# article1=input()
# article =article1.strip()
# space=0
# for i in range(len(article1)):
#     if article1[i]==' ':
#         space+=1
#     else:
#         break
#
# # 按空格分割成单词列表
# words = article.split()
#
# count = 0          # 出现次数
# first_pos = -1     # 第一次出现的位置
#
# # 遍历每个单词及其索引
# for i, word in enumerate(words):
#     if word.lower() == pattern:
#         count += 1
#         if first_pos == -1:  # 第一次匹配
#             # 计算该单词在原文中的起始位置
#             # 前 i 个单词的总长度 + i 个空格（因为 i 个单词之间有 i 个空格）
#             pos = sum(len(words[j]) for j in range(i)) + i+space
#             first_pos = pos
#
# # 输出结果
# if count > 0:
#     print(count, first_pos,end='')
# else:
#     print(-1)