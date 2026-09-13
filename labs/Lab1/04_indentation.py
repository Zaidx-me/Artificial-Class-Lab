# Lab 1: Indentation
# Python uses spaces at the start of a line to show code blocks

x = 10
if x > 5:
    print("x is greater than 5")   # this line is inside the if block
    print("x is positive")         # so is this one

# for loop
for i in range(3):
    print("Number:", i)

# while loop
count = 3
while count > 0:
    print(count)
    count = count - 1

# function
def greet(name):
    print("Hello,", name)

greet("Alice")
greet("Bob")