s1=input('输入所需检索的内容（纯英文不论大小写）：')
word=input('输入要统计的字符：')
word1=word.lower()
print('{0}在{1}中出现了{2}次'.format(word,s1,s1.lower().count(word1)))