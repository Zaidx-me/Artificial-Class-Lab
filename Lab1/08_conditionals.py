# Lab 1: Conditional Statements
# Comparison operators and if / elif / else

a = 10
b = 20

print(a == b)   # False - equal
print(a != b)   # True  - not equal
print(a < b)    # True  - less than
print(a <= b)   # True  - less than or equal
print(b > a)    # True  - greater than
print(b >= a)   # True  - greater than or equal

# if statement
age = 18
if age >= 18:
    print("You are an adult")

# if / else
number = 7
if number % 2 == 0:
    print("Even")
else:
    print("Odd")

# if / elif / else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print("Grade:", grade)

# and / or / not
temperature = 25
is_sunny = True

if temperature > 20 and is_sunny:
    print("Great day for a picnic!")

if not is_sunny:
    print("Take an umbrella")