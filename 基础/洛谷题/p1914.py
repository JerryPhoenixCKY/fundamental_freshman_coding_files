
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
    return ciphertext

def main():
    key=int(input())
    plaintext = input()

    encrypted = caesar_cipher(plaintext, key)
    print(encrypted)
if __name__ == "__main__":
    main()
