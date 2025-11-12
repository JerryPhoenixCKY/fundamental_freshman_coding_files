import re

def remove_english_from_file(input_file_path, output_file_path=None):
    """
    从txt文件中删除所有英文字符，只保留中文句子
    
    Args:
        input_file_path: 输入文件路径
        output_file_path: 输出文件路径（可选，默认为原文件名_cleaned.txt）
    """
    try:
        # 读取原文件
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式删除所有英文字母（大小写）、英文标点符号和
        # \u4e00-\u9fff 是中文字符的Unicode范围
        chinese_only = re.sub(r'[a-zA-Z\s\.,;:\'"!?@#$%^&*()\-=+_\[\]{}|\\<>\/`~]', '', content)
        
        # 进一步清理，只保留中文字符和中文标点符号
        chinese_only = re.sub(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', '', chinese_only)
        
        # 去除多余的空白行
        chinese_only = re.sub(r'\n+', '\n', chinese_only).strip()
        
        # 如果没有指定输出文件路径，则默认为原文件名_cleaned.txt
        if output_file_path is None:
            if input_file_path.endswith('.txt'):
                output_file_path = input_file_path[:-4] + '_cleaned.txt'
            else:
                output_file_path = input_file_path + '_cleaned.txt'
        
        # 写入新文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(chinese_only)
        
        print(f"处理完成！结果已保存到: {output_file_path}")
        return chinese_only
        
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file_path}")
        return None
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")
        return None

def main():
    """
    主函数 - 提供交互式界面
    """
    print("=== TXT文件英文字符删除工具 ===")
    input_path = input("请输入要处理的txt文件路径: ").strip().strip('"')
    
    # 询问是否指定输出文件路径
    output_choice = input("是否要指定输出文件路径？(y/n，默认为n): ").strip().lower()
    output_path = None
    
    if output_choice == 'y':
        output_path = input("请输入输出文件路径: ").strip().strip('"')

    result = remove_english_from_file(input_path, output_path)
    
    if result is not None:
        print("\n提取到的中文内容预览:")
        preview = result[:20]  # 只显示前200个字符作为预览
        print(preview)
        if len(result) > 20:
            print("...")
        print(f"\n总字符数: {len(result)}")

if __name__ == "__main__":
    main()



