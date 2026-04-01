def merge_sort(arr):
    """
    归并排序主函数（入口）
    :param arr: 待排序的列表
    :return: 返回一个新的已排序列表（不修改原列表）
    """
    if len(arr) <= 1:
        return arr  # 基线条件：单个元素或空列表已有序

    # === 分解（Divide）===
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])  # 递归排序左半部分
    right_half = merge_sort(arr[mid:])  # 递归排序右半部分

    # === 合并（Conquer）===
    return merge(left_half, right_half)


def merge(left, right):
    """
    合并两个已排序的列表，返回一个新的有序列表
    """
    result = []
    i = j = 0

    # 比较两个列表的当前元素，将较小者加入结果
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 将剩余元素（如果有）全部追加到结果末尾
    result.extend(left[i:])
    result.extend(right[j:])

    return result


# ================== 测试 ==================
if __name__ == "__main__":
    data = [38, 27, 43, 3, 9, 82, 10]
    print("原始数组:", data)
    sorted_data = merge_sort(data)
    print("归并排序后:", sorted_data)