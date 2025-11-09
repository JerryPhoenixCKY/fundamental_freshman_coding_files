# 简易计算器 —— 支持多数字四则运算

def parse_expression(expr):
    """
    解析表达式字符串，返回数字列表和运算符列表
    例如：'1+2*3' → nums=[1,2,3], ops=['+','*']
    """
    nums = []      # 存放数字
    ops = []       # 存放运算符
    num_str = ""   # 临时存储当前数字的字符串

    # 遍历每一个字符
    for char in expr:
        if char in '+-*/':  # 如果是运算符
            # 把之前累积的数字字符串转成浮点数存入 nums
            if num_str != "":
                nums.append(float(num_str))
                num_str = ""  # 清空，准备下一个数字
            ops.append(char)  # 存入运算符
        else:
            # 如果是数字或小数点，累积到 num_str
            num_str += char

    # 循环结束后，最后一个数字还没存入
    if num_str != "":
        nums.append(float(num_str))

    return nums, ops


def calculate(nums, ops):
    """
    根据数字列表和运算符列表进行计算
    遵循先乘除后加减的原则
    """
    # 第一步：处理所有 * 和 /
    i = 0
    while i < len(ops):
        op = ops[i]
        if op in '*/':  # 如果是乘除法
            try:
                # 取出左右两个数字
                left = nums[i]
                right = nums[i + 1]

                # 根据运算符计算
                if op == '*':
                    result = left * right
                else:  # op == '/'
                    if right == 0:
                        raise ZeroDivisionError("除数不能为零！")
                    result = left / right

                # 用结果替换左边数字，删除右边数字和当前运算符
                nums[i] = result
                del nums[i + 1]
                del ops[i]
                # 注意：删除后索引不变，因为列表缩短了，所以下一轮仍检查当前位置
            except ZeroDivisionError as e:
                print(f"❌ 计算错误：{e}")
                return None
            except Exception as e:
                print(f"❌ 未知错误：{e}")
                return None
        else:
            # 如果不是乘除，跳过
            i += 1

    # 第二步：处理所有 + 和 -
    i = 0
    while i < len(ops):
        op = ops[i]
        if op in '+-':
            try:
                left = nums[i]
                right = nums[i + 1]

                if op == '+':
                    result = left + right
                else:  # op == '-'
                    result = left - right

                nums[i] = result
                del nums[i + 1]
                del ops[i]
            except Exception as e:
                print(f"❌ 计算过程中出错：{e}")
                return None
        else:
            i += 1  # 理论上不会发生，因为只剩+-了

    # 最终 nums 里只剩一个数，就是结果
    return nums[0]


def main():
    """
    主函数：接收用户输入，调用解析和计算函数，输出结果
    """
    print("简易计算器（支持多数字四则运算）")
    print("示例：1+2*3-4/2")
    print("输入 'quit' 退出程序\n")

    while True:
        expr = input("请输入算式：").strip()

        if expr.lower() == 'quit':
            print("👋 程序已退出，再见！")
            break

        # 如果输入为空，跳过
        if expr == "":
            continue

        try:
            # 解析表达式
            nums, ops = parse_expression(expr)
        except ValueError:
            print("❌ 输入格式错误，请输入合法算式（如：3+5*2）")
            continue
        except Exception as e:
            print(f"❌ 解析时出错：{e}")
            continue

        # 检查解析后数字和运算符数量是否匹配
        if len(nums) != len(ops) + 1:
            print("❌ 表达式格式错误（运算符和数字数量不匹配）")
            continue

        # 开始计算
        result = calculate(nums, ops)

        if result is not None:
            # 如果是整数，显示为整数；否则保留小数
            if result == int(result):
                print(f"✅ 结果：{int(result)}")
            else:
                print(f"✅ 结果：{result}")
        else:
            print("❌ 无法完成计算，请检查表达式。")


# 启动程序
if __name__ == "__main__":
    main()


