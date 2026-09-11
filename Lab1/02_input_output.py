# Lab 1: Input and Output
# This program demonstrates input() and print() functions

# Basic input - reads a string from user
name = input("Enter your name: ")
print("Hello, " + name + "!")

# Input with prompt and storing as different types
age = input("Enter your age: ")
print("Your age is:", age)
print("Type of age:", type(age))

# Converting input to integer
age_int = int(input("Enter your age (as number): "))
print("Next year you will be:", age_int + 1)

# Input with type conversion to float
height = float(input("Enter your height in meters: "))
print("Your height in centimeters:", height * 100)

# Multiple inputs in one line
print("\nEnter two numbers:")
num1 = int(input("First number: "))
num2 = int(input("Second number: "))
print(f"Sum: {num1 + num2}")
print(f"Difference: {num1 - num2}")
print(f"Product: {num1 * num2}")

# Using input() with eval for complex expressions
print("\nEnter a mathematical expression (e.g., 2+3*4):")
expr = input("Expression: ")
print("Result:", eval(expr))
