"""
    凯撒密码加密函数
    :param plaintext: 明文字符串
    :param key: 密钥（整数，可正可负）
    :return: 加密后的暗文字符串

    str.isupper()	所有字母都是大写，且至少有一个字母
    str.islower()	所有字母都是小写，且至少有一个字母
    str.istitle()	每个单词首字母大写（如 "Hello World"）
    str.isalpha()	所有字符都是字母（不分大小写）
    str.isalnum()	所有字符是字母或数字
"""
def caesar_cipher(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isupper():  # 处理大写字母 A-Z

            shifted = (ord(char) - ord('A') + key) % 26
            new_char = chr(shifted + ord('A'))
            ciphertext += new_char
        elif char.islower():  # 处理小写字母 a-z
            # ord('a') = 97
            shifted = (ord(char) - ord('a') + key) % 26
            new_char = chr(shifted + ord('a'))
            ciphertext += new_char
        else:
            shifted = (ord(char) - ord('0')+key)%10
            new_char = chr(shifted + ord('0'))
            ciphertext += new_char

    return ciphertext

def main():
    print("=== 凯撒密码加密器 ===")
    plaintext = input("请输入明文：")
    try:
        key = int(input("请输入密钥（整数，如3或-5）："))
    except ValueError:
        print("密钥必须是整数！")
        exit()
    encrypted = caesar_cipher(plaintext, key)
    print(f"加密结果（暗文）：{encrypted}")
if __name__ == "__main__":
    main()
