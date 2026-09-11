# Lab 1: Lists
# This program demonstrates Python list operations

print("=" * 50)
print("CREATING LISTS")
print("=" * 50)

# Empty list
empty_list = []
print(f"Empty list: {empty_list}")

# List with values
numbers = [1, 2, 3, 4, 5]
print(f"Numbers: {numbers}")

# Mixed type list
mixed = [1, "Hello", 3.14, True, None]
print(f"Mixed types: {mixed}")

# Nested list
nested = [[1, 2], [3, 4], [5, 6]]
print(f"Nested list: {nested}")

# Using list() constructor
from_string = list("Python")
print(f"From string: {from_string}")

# Using range
from_range = list(range(1, 6))
print(f"From range: {from_range}")

print("\n" + "=" * 50)
print("LIST INDICES")
print("=" * 50)

colors = ["RED", "Blue", "Green", "Black"]
print(f"Color list: {colors}")
print(f"Number of colors: {len(colors)}")

# Positive indices (from left)
print("\nPositive indices:")
for i in range(len(colors)):
    print(f"  colors[{i}] = {colors[i]}")

# Negative indices (from right)
print("\nNegative indices:")
for i in range(-len(colors), 0):
    print(f"  colors[{i}] = {colors[i]}")

# Accessing specific elements
print(f"\nFirst color: {colors[0]}")
print(f"Last color: {colors[-1]}")
print(f"Third color: {colors[2]}")

print("\n" + "=" * 50)
print("LIST SLICING")
print("=" * 50)

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"Original list: {numbers}")

# Basic slicing [start:end]
print(f"\nSlicing examples:")
print(f"  numbers[2:5] = {numbers[2:5]}")  # [2, 3, 4]
print(f"  numbers[:4] = {numbers[:4]}")    # [0, 1, 2, 3]
print(f"  numbers[6:] = {numbers[6:]}")    # [6, 7, 8, 9]
print(f"  numbers[:] = {numbers[:]}")      # Full copy

# Negative slicing
print(f"\nNegative slicing:")
print(f"  numbers[-3:] = {numbers[-3:]}")  # [7, 8, 9]
print(f"  numbers[:-2] = {numbers[:-2]}")  # [0, 1, 2, 3, 4, 5, 6, 7]
print(f"  numbers[-4:-1] = {numbers[-4:-1]}")  # [6, 7, 8]

# Step slicing [start:end:step]
print(f"\nStep slicing:")
print(f"  numbers[::2] = {numbers[::2]}")    # Every other element
print(f"  numbers[1::2] = {numbers[1::2]}")  # Odd indices
print(f"  numbers[::-1] = {numbers[::-1]}")   # Reverse list

# Slicing with out-of-range indices (no error!)
print(f"\nOut-of-range slicing (safe):")
print(f"  numbers[2:100] = {numbers[2:100]}")
print(f"  numbers[-100:3] = {numbers[-100:3]}")

print("\n" + "=" * 50)
print("LIST OPERATIONS")
print("=" * 50)

# Adding elements
fruits = ["apple", "banana"]
print(f"Original: {fruits}")

fruits.append("cherry")
print(f"After append('cherry'): {fruits}")

fruits.insert(1, "orange")
print(f"After insert(1, 'orange'): {fruits}")

# Removing elements
fruits.remove("banana")
print(f"After remove('banana'): {fruits}")

popped = fruits.pop()
print(f"After pop(): {fruits}, popped: {popped}")

# Modifying elements
fruits[0] = "BLUEBERRY"
print(f"After modifying index 0: {fruits}")

# List methods
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"\nList: {numbers}")
print(f"  Length: {len(numbers)}")
print(f"  Min: {min(numbers)}")
print(f"  Max: {max(numbers)}")
print(f"  Sum: {sum(numbers)}")
print(f"  Count of 1: {numbers.count(1)}")
print(f"  Index of 5: {numbers.index(5)}")

numbers.sort()
print(f"  After sort(): {numbers}")

numbers.reverse()
print(f"  After reverse(): {numbers}")

# Concatenation and repetition
list1 = [1, 2, 3]
list2 = [4, 5, 6]
print(f"\n{list1} + {list2} = {list1 + list2}")
print(f"{list1} * 3 = {list1 * 3}")

# Membership testing
print(f"\nMembership testing:")
print(f"  3 in {list1}: {3 in list1}")
print(f"  7 in {list1}: {7 in list1}")
