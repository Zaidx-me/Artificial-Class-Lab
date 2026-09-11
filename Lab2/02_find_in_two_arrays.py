# 02_find_in_two_arrays.py
# Search for one element across TWO arrays and report exactly where it is
# found: only in the first array, only in the second array, in both, or
# in neither.


def linear_search(items, target):
    """Return the index of target in items, or -1 if it is not found."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


def find_in_two_arrays(first, second, target):
    """Search target in both arrays and describe where it was found."""
    index_first = linear_search(first, target)
    index_second = linear_search(second, target)

    if index_first != -1 and index_second != -1:
        return (f"{target} found in BOTH arrays "
                f"(first[{index_first}], second[{index_second}])")
    elif index_first != -1:
        return f"{target} found only in the FIRST array at index {index_first}"
    elif index_second != -1:
        return (f"{target} found only in the SECOND array "
                f"at index {index_second}")
    else:
        return f"{target} is not present in either array"


def main():
    array_a = [3, 7, 12, 25, 42]
    array_b = [8, 12, 25, 50, 77]

    print("Array A:", array_a)
    print("Array B:", array_b)
    print()

    # 25 -> in both, 3 -> only first, 8 -> only second, 99 -> neither
    for target in [25, 3, 8, 99]:
        print(find_in_two_arrays(array_a, array_b, target))


if __name__ == "__main__":
    main()