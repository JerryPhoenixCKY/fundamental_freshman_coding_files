def binary_to_k(binary_str, k):
    """
    将二进制字符串转换为K进制字符串。

    :param binary_str: 输入的二进制数字符串 (例如 '1011')
    :param k: 目标进制 (2 < k <= 16)
    :return: 转换后的K进制数字符串，如果输入无效则返回错误信息
    """
    # 检查输入是否为有效的二进制字符串
    if not all(c in '01' for c in binary_str):
        return "错误: 输入不是有效的二进制数。"

    if not (2 < k <= 16):
        return "错误: K必须在3到16之间（包含3和16）。"

    # 定义数字到字符的映射，支持到16进制
    digits = "0123456789ABCDEF"

    # 将二进制字符串转换为十进制整数
    decimal_value = 0
    power = 0
    for digit in reversed(binary_str):
        decimal_value += int(digit) * (2 ** power)
        power += 1

    # 如果十进制值为0，直接返回'0'
    if decimal_value == 0:
        return '0'

    # 将十进制数转换为K进制
    k_base_digits = []
    temp_value = decimal_value
    while temp_value > 0:
        remainder = temp_value % k
        k_base_digits.append(digits[remainder])
        temp_value = temp_value // k

    # 反转列表以获得正确的顺序
    k_base_digits.reverse()

    # 将列表合并为字符串并返回
    return ''.join(k_base_digits)


def k_to_binary(k_str, k):
    """
    将K进制字符串转换为二进制字符串。

    :param k_str: 输入的K进制数字符串 (例如 'B')
    :param k: 输入的进制 (2 < k <= 16)
    :return: 转换后的二进制数字符串，如果输入无效则返回错误信息
    """
    # 检查K的范围
    if not (2 < k <= 16):
        return "错误: K必须在3到16之间（包含3和16）。"

    # 定义字符到数字的映射
    digit_map = {char: i for i, char in enumerate("0123456789ABCDEF")}

    # 检查输入字符串中的所有字符是否有效
    for char in k_str.upper():
        if char not in digit_map or digit_map[char] >= k:
            return f"错误: '{char}' 不是有效的{k}进制数字。"

    # 将K进制字符串转换为十进制整数
    decimal_value = 0
    power = 0
    for digit in reversed(k_str.upper()):
        decimal_value += digit_map[digit] * (k ** power)
        power += 1

    # 如果十进制值为0，直接返回'0'
    if decimal_value == 0:
        return '0'

    # 将十进制数转换为二进制
    binary_digits = []
    temp_value = decimal_value
    while temp_value > 0:
        remainder = temp_value % 2
        binary_digits.append(str(remainder))
        temp_value = temp_value // 2

    # 反转列表以获得正确的顺序
    binary_digits.reverse()

    # 将列表合并为字符串并返回
    return ''.join(binary_digits)




def main():
    """
    主函数，提供用户交互界面。
    """
    print("--- K进制与二进制互换程序 ---")
    while True:
        print("\n请选择操作:")
        print("1. 二进制 转 K进制")
        print("2. K进制 转 二进制")
        print("3. 退出")

        choice = input("请输入选项 (1/2/3): ").strip()

        if choice == '1':
            try:
                binary_input = input("请输入二进制数: ").strip()
                k_input = int(input("请输入目标进制K (3-16): ").strip())
                result = binary_to_k(binary_input, k_input)
                print(f"二进制 {binary_input} 转 {k_input}进制 的结果是: {result}")
            except ValueError:
                print("错误: 请输入有效的数字。")

        elif choice == '2':
            try:
                k_input_str = input("请输入K进制数: ").strip()
                k_input = int(input("请输入K进制的基数K (3-16): ").strip())
                result = k_to_binary(k_input_str, k_input)
                print(f"{k_input}进制 {k_input_str} 转 二进制 的结果是: {result}")
            except ValueError:
                print("错误: 请输入有效的数字。")

        elif choice == '3':
            print("程序退出。")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()

