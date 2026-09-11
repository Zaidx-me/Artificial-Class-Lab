# 01_linear_search.py
# Linear Search - find the position of a target element in a list by
# checking every element in order, from the first to the last.


def linear_search(items, target):
    """Return the index of target in items, or -1 if it is not found."""
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1


def linear_search_enumerate(items, target):
    """Same search written with enumerate() for a cleaner loop."""
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def find_all_occurrences(items, target):
    """Return a list of every index where target appears."""
    return [i for i, value in enumerate(items) if value == target]


def main():
    numbers = [10, 23, 45, 70, 11, 15, 70, 20]

    print("List:", numbers)

    # Simple linear search (value IS present)
    target = 70
    index = linear_search(numbers, target)
    print(f"Searching for {target}...")
    if index != -1:
        print(f"  Found at index {index}")
    else:
        print("  Not found")

    # Value is NOT present -> returns -1
    missing = 99
    if linear_search(numbers, missing) == -1:
        print(f"Searching for {missing}...")
        print("  Not found (returned -1)")

    # Search using enumerate() version
    print(f"enumerate version, target {11}: index = "
          f"{linear_search_enumerate(numbers, 11)}")

    # All occurrences of a repeated value
    print(f"{target} appears at indices: {find_all_occurrences(numbers, target)}")

    # Works on strings too
    fruits = ["apple", "banana", "cherry"]
    print(f"'banana' in {fruits}: index = "
          f"{linear_search(fruits, 'banana')}")


if __name__ == "__main__":
    main()