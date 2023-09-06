def binary_search(lst, item):
    low = 0
    high = len(lst) - 1
    while low <= high:
        middle = (low + high) // 2
        if lst[middle] == item:
            return middle
        if item > lst[middle]:
            low = middle + 1
        else:
            high = middle - 1


def intersection_sort(lst):
    def find_min_elem(lst2):
        element = lst2[0]
        index = 0
        for i in range(len(lst2)):
            if lst2[i] < element:
                element = lst2[i]
                index = i
        return index, element

    lst = lst.copy()
    sort_result = []
    while lst:
        index, elem = find_min_elem(lst)
        del lst[index]
        sort_result.append(elem)

    return sort_result
