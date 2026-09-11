# Lab 1: Indentation
# This program demonstrates Python's indentation rules

# Python uses indentation to define code blocks
# Unlike C/C++ which use braces {}

# Example 1: Basic indentation with if statement
x = 10
if x > 5:
    print("x is greater than 5")  # This is inside the if block
    print("x is definitely positive")  # Also inside the if block

# Example 2: Nested indentation
y = 20
if y > 10:
    print("y is greater than 10")
    if y > 15:
        print("y is also greater than 15")  # Nested block

# Example 3: Indentation with for loop
print("\nCounting from 1 to 5:")
for i in range(1, 6):
    print(i, end=" ")  # Print on same line

# Example 4: Indentation with while loop
print("\n\nCountdown:")
count = 5
while count > 0:
    print(count, end=" ")
    count -= 1
print("Done!")

# Example 5: Functions and indentation
def greet(name):
    """Demonstrate function indentation"""
    message = "Hello, " + name + "!"
    print(message)
    return message

# Calling the function
greet("Alice")
greet("Bob")

# Important rules:
# 1. Use 4 spaces per indentation level (recommended)
# 2. Never mix tabs and spaces
# 3. All statements in the same block must have same indentation
# 4. Maximum line length should be 79 characters
