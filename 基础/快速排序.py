def quickort(L, low, high):
    if low < high:
        # 分区操作，返回 pivot 的最终位置
        pivot_index = partition(L, low, high)
        # 递归排序左右两部分
        quickort(L, low, pivot_index - 1)
        quickort(L, pivot_index + 1, high)
    return L

def partition(L, low, high):
    pivot = L[low]  # 选择第一个元素作为基准
    i = low + 1      # 左指针
    j = high         # 右指针

    while True:
        # 从左向右找大于等于 pivot 的元素
        while i <= j and L[i] <= pivot:
            i += 1
        # 从右向左找小于 pivot 的元素
        while i <= j and L[j] >= pivot:
            j -= 1
        if i > j:
            break
        # 交换 L[i] 和 L[j]
        L[i], L[j] = L[j], L[i]
    # 将 pivot 放到正确位置
    L[low], L[j] = L[j], L[low]
    return j
############################################################################################
def quicksort(lst):
    if len(lst) <= 1:
        return lst
    pivot = lst[0]
    left = [x for x in lst[1:] if x <= pivot]
    right = [x for x in lst[1:] if x > pivot]
    return quicksort(left) + [pivot] + quicksort(right)

# 使用示例
L = [6, 5, 3, 10, 12, 2, 4]
print(quickort(L,0,6))  # 输出: [2, 3, 4, 5, 6, 10, 12]