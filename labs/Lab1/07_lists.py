# Lab 1: Lists
# A list stores many values in one variable

fruits = ["apple", "banana", "cherry"]
print(fruits)

# Indexing - starts from 0
print(fruits[0])    # first item
print(fruits[-1])   # last item

# Slicing - a part of the list
print(fruits[0:2])  # first two items

# Adding and removing items
fruits.append("mango")
print(fruits)

fruits.remove("banana")
print(fruits)

# Loop through the list
for fruit in fruits:
    print(fruit)

# Check if an item is in the list
print("apple" in fruits)
print("grapes" in fruits)

# Useful functions
numbers = [5, 2, 8, 1]
print(len(numbers))    # how many items
print(min(numbers))    # smallest value
print(max(numbers))    # biggest value
print(sum(numbers))    # total of all values

numbers.sort()         # sorts the list
print(numbers)