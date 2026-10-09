# Binary search implementation in Python (from scratch, including the sort)

def bubble_sort(array):
    n = len(array)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]


def binary_search(array, target):
    low = 0
    high = len(array) - 1
    while low <= high:
        mid = (low + high) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

array = [23, 56, 70, 88, 90, 99, 12, 34, 9, 5]
bubble_sort(array)          # sorting done manually, not with array.sort()
print("Sorted array:", array)
target = int(input("Enter the number to search: "))
result = binary_search(array, target)
if result != -1:
    print("Element found at the index:", result)
else:
    print("Element not found")