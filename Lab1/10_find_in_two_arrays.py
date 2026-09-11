# 10_find_in_two_arrays.py
# Search one value across two arrays and report where it was found.


def find_in_two_arrays(first, second, target):
    """Return a message describing where target appears in the arrays."""
    first_index = -1
    second_index = -1

    for i in range(len(first)):
        if first[i] == target:
            first_index = i

    for i in range(len(second)):
        if second[i] == target:
            second_index = i

    if first_index != -1 and second_index != -1:
        return (f"{target} found in both arrays "
                f"(index {first_index} and {second_index})")
    elif first_index != -1:
        return f"{target} found only in the first array at index {first_index}"
    elif second_index != -1:
        return (f"{target} found only in the second array "
                f"at index {second_index}")
    else:
        return f"{target} not found in either array"


def main():
    array_a = [3, 7, 12, 25, 42]
    array_b = [8, 12, 25, 50, 77]

    print("Array A:", array_a)
    print("Array B:", array_b)
    print()

    print(find_in_two_arrays(array_a, array_b, 25))
    print(find_in_two_arrays(array_a, array_b, 3))
    print(find_in_two_arrays(array_a, array_b, 8))
    print(find_in_two_arrays(array_a, array_b, 99))


if __name__ == "__main__":
    main()