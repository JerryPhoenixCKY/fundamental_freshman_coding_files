import re

def highlight_keywords(text, keywords, case_sensitive=False):
    """
    在文本中高亮关键词（用【】包围），返回高亮后的文本和匹配结果。
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    found_info = {}

    # 对每个关键词进行匹配和替换
    highlighted_text = text
    for kw in keywords:
        if not kw.strip():  # 跳过空关键词
            continue
        # 转义关键词中的特殊正则字符
        escaped_kw = re.escape(kw)
        # 检查是否存在匹配
        matches = re.findall(escaped_kw, text, flags=flags)
        found_info[kw] = len(matches) > 0

        # 高亮：用【】包围所有匹配项（非破坏性替换）
        highlighted_text = re.sub(
            escaped_kw,
            lambda m: f"【{m.group()}】",
            highlighted_text,
            flags=flags
        )

    return highlighted_text, found_info

def main():
    print("请输入大段文字（可多行，输入结束后空行回车）：")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    text = "\n".join(lines)

    print("\n请输入关键词（多个关键词用空格或逗号分隔）：")
    keyword_input = input().strip()
    # 支持空格或逗号分隔
    if ',' in keyword_input:
        keywords = [kw.strip() for kw in keyword_input.split(',') if kw.strip()]
    else:
        keywords = [kw.strip() for kw in keyword_input.split() if kw.strip()]

    if not keywords:
        print("未输入有效关键词。")
        return

    # 执行检索
    highlighted, results = highlight_keywords(text, keywords, case_sensitive=False)

    # 输出结果
    print("\n" + "="*50)
    print("🔍 检索结果：")
    for kw, found in results.items():
        status = "✅ 找到" if found else "❌ 未找到"
        print(f"  - 关键词 '{kw}': {status}")

    print("\n📄 原文（已高亮匹配项）：")
    print(highlighted)

if __name__ == "__main__":
    main()