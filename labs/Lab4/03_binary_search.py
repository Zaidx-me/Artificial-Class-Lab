# Binary search implementation in Python

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
array.sort()
print("Sorted array:", array)
target = int(input("Enter the number to search: "))
result = binary_search(array, target)
if result != -1:
    print("Element found at the index:", result)
else:
    print("Element not found")