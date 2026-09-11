# Lab 1: Linear Search
# Find the position of a value in a list

def linear_search(items, target):
    # Check each item one by one
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1   # not found

numbers = [10, 23, 45, 70, 11, 15, 20]

print("45 is at index:", linear_search(numbers, 45))
print("99 is at index:", linear_search(numbers, 99))   # -1 means not found