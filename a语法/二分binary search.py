def binary_search(arr, target):
    """
    在已排序列表 arr 中查找 target 的索引。
    如果找到，返回其索引；否则返回 -1。

    算法本质：每次将搜索区间缩小一半（"二分"）。
    时间复杂度：O(log n)
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        # 防止 (left + right) 溢出（在 Python 中不必要，但在 C/Java 中重要）
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid  # 找到目标，返回索引
        elif arr[mid] < target:
            left = mid + 1  # 目标在右半部分
        else:
            right = mid - 1  # 目标在左半部分

    return -1  # 未找到


# 示例使用
if __name__ == "__main__":
    sorted_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 7

    index = binary_search(sorted_list, target)
    if index != -1:
        print(f"元素 {target} 在索引 {index} 处找到。")
    else:
        print(f"元素 {target} 未找到。")


#####################################
#找左侧第一个目标数，右侧最后一个同理，为变式


def binary_search_first(arr, target):
    """
    在已排序数组 arr 中查找第一个等于 target 的元素的索引。
    如果不存在，返回 -1。

    时间复杂度: O(log n)
    空间复杂度: O(1)
    """
    left = 0
    right = len(arr) - 1
    first_pos = -1  # 用于记录第一个匹配的位置

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            first_pos = mid  # 记录当前位置
            right = mid - 1  # ⚠️ 关键：继续向左搜索更早的匹配
        elif arr[mid] < target:
            left = mid + 1  # 目标在右半部分
        else:
            right = mid - 1  # 目标在左半部分

    return first_pos


# ================== 测试用例 ==================
if __name__ == "__main__":
    test_cases = [
        ([1, 2, 2, 2, 3, 4, 5], 2, 1),
        ([1, 1, 1, 1, 1], 1, 0),
        ([1, 3, 5, 7], 3, 1),
        ([1, 3, 5, 7], 6, -1),
        ([], 5, -1),
        ([2, 2, 2, 2], 2, 0),
        ([1, 2, 3, 4, 5], 1, 0),
        ([1, 2, 3, 4, 5], 5, 4),
    ]

    for arr, target, expected in test_cases:
        result = binary_search_first(arr, target)
        status = "✅" if result == expected else "❌"
        print(f"{status} 数组: {arr}, 目标: {target} → 结果: {result} (期望: {expected})")