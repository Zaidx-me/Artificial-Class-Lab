# Lab 1: Common Values in Two Arrays
# Find the values that are in both arrays

def common_elements(first, second):
    common = []
    for value in first:
        if value in second and value not in common:
            common.append(value)
    return common

array_a = [1, 2, 3, 4, 5]
array_b = [4, 5, 6, 7, 8]

print("Common elements:", common_elements(array_a, array_b))