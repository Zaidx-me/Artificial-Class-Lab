# 11_common_in_two_arrays.py
# Find the values that appear in both arrays.


def common_elements(first, second):
    """Return the list of values present in both arrays."""
    common = []
    for value in first:
        if value in second and value not in common:
            common.append(value)
    return common


def main():
    array_a = [1, 2, 3, 4, 5]
    array_b = [4, 5, 6, 7, 8]

    print("Array A:", array_a)
    print("Array B:", array_b)
    print("Common elements:", common_elements(array_a, array_b))


if __name__ == "__main__":
    main()