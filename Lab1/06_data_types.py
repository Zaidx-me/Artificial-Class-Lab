# Lab 1: Data Types
# Numbers, Booleans, Strings, and Type Casting

# Numbers
age = 21              # int - whole number
pi = 3.14             # float - decimal number
c = 3 + 4j            # complex - has a real and imaginary part

print(age, type(age))
print(pi, type(pi))
print(c, type(c))

# Booleans - True or False
is_student = True
print(is_student, type(is_student))
print(True + True)    # True behaves like 1

# Strings
name = "Python"
print(name, type(name))

print(len(name))      # length of the string
print(name[0])        # first character
print(name[-1])       # last character
print(name[0:3])      # slicing - characters 0 to 2

# Strings cannot be changed after creation
# name[0] = "p"  # this gives an error

# Escape sequences
print("Line1\nLine2")   # \n is a newline
print("Tab\there")      # \t is a tab

# Type casting - changing one type to another
print(int("42") + 1)    # string to int
print(float("3.14"))    # string to float
print(str(42) + "!")    # int to string