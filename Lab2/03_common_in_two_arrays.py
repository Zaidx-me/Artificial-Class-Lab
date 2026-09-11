# 03_common_in_two_arrays.py
# Find the common elements (intersection) shared by two arrays, using
# three different approaches.


def common_brute_force(first, second):
    """Nested loops - simple but slow for large arrays (O(n*m))."""
    common = []
    for value in first:
        if value in second and value not in common:
            common.append(value)
    return common


def common_with_sets(first, second):
    """Sets - fastest approach; order is not preserved."""
    return list(set(first) & set(second))


def common_ordered(first, second):
    """Sets for speed, but keeps the order of the first array."""
    second_set = set(second)
    seen = set()
    common = []
    for value in first:
        if value in second_set and value not in seen:
            common.append(value)
            seen.add(value)
    return common


def main():
    array_a = [1, 2, 3, 4, 5, 5]
    array_b = [4, 5, 6, 7, 8]

    print("Array A:", array_a)
    print("Array B:", array_b)
    print()

    print("Common, brute force (nested loops):", common_brute_force(array_a, array_b))
    print("Common, using sets:                ", common_with_sets(array_a, array_b))
    print("Common, ordered (keeps A's order): ", common_ordered(array_a, array_b))


if __name__ == "__main__":
    main()