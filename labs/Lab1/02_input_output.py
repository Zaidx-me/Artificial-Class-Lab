# Lab 1: Input and Output
# input() reads from the user, print() writes to the screen

name = input("Enter your name: ")
print("Hello, " + name + "!")

# input() always returns a string
age = input("Enter your age: ")
print("Your age is:", age)
print("Type of age:", type(age))

# Convert the string to an int so we can do math
age = int(input("Enter your age again: "))
print("Next year you will be:", age + 1)

# Two numbers from the user
num1 = int(input("First number: "))
num2 = int(input("Second number: "))
print("Sum:", num1 + num2)
print("Product:", num1 * num2)