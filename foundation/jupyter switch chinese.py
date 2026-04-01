import nbformat
from deep_translator import GoogleTranslator
import os
import time

def translate_notebook(input_filepath, output_filepath):
    print(f"正在读取 Notebook: {input_filepath}")
    
    # 读取 Jupyter Notebook
    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print("未找到指定的文件，请检查路径。")
        return

    # 初始化 Google 翻译器 (自动检测语言 -> 简体中文)
    translator = GoogleTranslator(source='auto', target='zh-CN')
    
    # 遍历所有的单元格
    total_cells = len(nb.cells)
    translated_count = 0
    
    print("开始翻译 Markdown 单元格...")
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            original_text = cell.source
            if original_text.strip(): # 如果文本不为空
                try:
                    # 注意：如果单次翻译文本超过 5000 字符可能会报错，对于超长 cell 可以考虑根据换行符分段翻译
                    if len(original_text) > 5000:
                        # 将长文本按换行符分段翻译
                        lines = original_text.split('\n')
                        translated_lines = []
                        for line in lines:
                            if line.strip():
                                translated_line = translator.translate(line)
                                translated_lines.append(translated_line)
                            else:
                                translated_lines.append(line)
                            time.sleep(0.1)  # 避免请求过于频繁
                        translated_text = '\n'.join(translated_lines)
                    else:
                        translated_text = translator.translate(original_text)
                    cell.source = translated_text
                    translated_count += 1
                    print(f"进度: 翻译了第 {i+1}/{total_cells} 个单元格")
                    time.sleep(0.5)  # 避免请求过于频繁
                except Exception as e:
                    print(f"翻译第 {i+1} 个单元格时出错: {e}")
                    print(f"跳过该单元格，继续处理下一个...")
    
    # 写入到新的 Notebook
    with open(output_filepath, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
        
    print(f"翻译完成！共翻译了 {translated_count} 个 Markdown 单元格。")
    print(f"新文件已保存至: {output_filepath}")

if __name__ == "__main__":
    # 配置你的输入和输出文件路径
    # 例如：
    # input_file = r"d:\primary coding files\您的英文笔记.ipynb"
    # output_file = r"d:\primary coding files\翻译后的笔记.ipynb"
    
    input_file = input("请输入要翻译的 .ipynb 文件路径: ").strip('\"\'')
    
    if os.path.exists(input_file) and input_file.endswith('.ipynb'):
        # 自动生成输出文件名
        directory, filename = os.path.split(input_file)
        name, ext = os.path.splitext(filename)
        output_file = os.path.join(directory, f"{name}_中文版{ext}")
        
        translate_notebook(input_file, output_file)
    else:
        print("输入路径无效，请确保输入的是存在的 .ipynb 文件。")