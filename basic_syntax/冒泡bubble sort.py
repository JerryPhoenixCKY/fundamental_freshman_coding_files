def bubble_sort(arr):
    """
    对列表 arr 进行冒泡排序（升序）
    :param arr: 待排序的列表
    :return: 原地排序，无返回值（或可返回 arr）
    """
    n = len(arr)
    # 外层循环：控制总共需要进行多少轮比较
    # 一共 n 个元素，最多需要 n-1 轮就能排好
    for i in range(n - 1):
        swapped = False  # 优化：记录本轮是否发生交换

        # 内层循环：在未排序部分中逐个比较相邻元素
        # 每轮结束后，最大的元素会“冒泡”到末尾
        # 所以每轮比较的范围可以缩小 1（即 n - 1 - i）
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                # 如果前一个元素大于后一个，则交换
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True  # 标记发生了交换

        # 优化：如果某一轮没有发生任何交换，说明数组已经有序，可以提前结束
        if not swapped:
            break


# 示例使用
if __name__ == "__main__":
    data = [64, 34, 25, 12, 22, 11, 90]
    print("原始列表:", data)
    bubble_sort(data)
    print("排序后列表:", data)

