# 09_linear_search.py
# Linear search: find the position of a value in a list by checking each
# element in order. Returns the index, or -1 when the value is not found.


def linear_search(items, target):
    """Return the index of target in items, or -1 if not found."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


def main():
    numbers = [10, 23, 45, 70, 11, 15, 20]

    print("List:", numbers)

    # Value that exists
    target = 45
    index = linear_search(numbers, target)
    if index != -1:
        print(f"{target} found at index {index}")
    else:
        print(f"{target} not found")

    # Value that does not exist
    target = 99
    index = linear_search(numbers, target)
    if index != -1:
        print(f"{target} found at index {index}")
    else:
        print(f"{target} not found")


if __name__ == "__main__":
    main()