# Lab 1: Find a Value in Two Arrays
# Search for one value and say which array(s) it is in

def find_in_two_arrays(first, second, target):
    first_index = -1
    second_index = -1

    for i in range(len(first)):
        if first[i] == target:
            first_index = i

    for i in range(len(second)):
        if second[i] == target:
            second_index = i

    if first_index != -1 and second_index != -1:
        print(target, "is in both arrays")
    elif first_index != -1:
        print(target, "is only in the first array")
    elif second_index != -1:
        print(target, "is only in the second array")
    else:
        print(target, "is in neither array")

array_a = [3, 7, 12, 25, 42]
array_b = [8, 12, 25, 50, 77]

find_in_two_arrays(array_a, array_b, 25)
find_in_two_arrays(array_a, array_b, 3)
find_in_two_arrays(array_a, array_b, 8)
find_in_two_arrays(array_a, array_b, 99)