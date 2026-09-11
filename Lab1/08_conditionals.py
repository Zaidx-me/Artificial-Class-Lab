# Lab 1: Conditional Statements
# This program demonstrates Python's comparison operators and if statements

print("=" * 50)
print("COMPARISON OPERATORS")
print("=" * 50)

a = 10
b = 20
c = 10

print(f"a = {a}, b = {b}, c = {c}")
print()

# Equals (==)
print(f"{a} == {b}: {a == b}")
print(f"{a} == {c}: {a == c}")

# Not equals (!=)
print(f"\n{a} != {b}: {a != b}")
print(f"{a} != {c}: {a != c}")

# Less than (<)
print(f"\n{a} < {b}: {a < b}")
print(f"{b} < {a}: {b < a}")

# Less than or equal (<=)
print(f"\n{a} <= {c}: {a <= c}")
print(f"{a} <= {b}: {a <= b}")
print(f"{b} <= {a}: {b <= a}")

# Greater than (>)
print(f"\n{b} > {a}: {b > a}")
print(f"{a} > {b}: {a > b}")

# Greater than or equal (>=)
print(f"\n{b} >= {a}: {b >= a}")
print(f"{a} >= {c}: {a >= c}")
print(f"{a} >= {b}: {a >= b}")

print("\n" + "=" * 50)
print("BASIC IF STATEMENTS")
print("=" * 50)

# Simple if statement
x = 25
print(f"\nx = {x}")

if x > 0:
    print("x is positive")

# if-else statement
print("\nChecking if number is even or odd:")
number = 17
print(f"number = {number}")

if number % 2 == 0:
    print(f"{number} is even")
else:
    print(f"{number} is odd")

# if-elif-else statement
print("\nDetermining grade:")
score = 85
print(f"score = {score}")

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Grade: {grade}")

print("\n" + "=" * 50)
print("NESTED CONDITIONALS")
print("=" * 50)

age = 25
has_license = True

print(f"age = {age}, has_license = {has_license}")

if age >= 18:
    print("You are an adult")
    if has_license:
        print("You can drive")
    else:
        print("You need to get a license")
else:
    print("You are a minor")
    print("You cannot drive yet")

print("\n" + "=" * 50)
print("COMBINING CONDITIONS")
print("=" * 50)

# Using 'and' operator
print("\nUsing 'and' operator:")
temperature = 25
is_sunny = True
print(f"temperature = {temperature}, is_sunny = {is_sunny}")

if temperature > 20 and is_sunny:
    print("Great day for a picnic!")

# Using 'or' operator
print("\nUsing 'or' operator:")
is_weekend = False
is_holiday = True
print(f"is_weekend = {is_weekend}, is_holiday = {is_holiday}")

if is_weekend or is_holiday:
    print("You don't have to work today!")

# Using 'not' operator
print("\nUsing 'not' operator:")
is_raining = False
print(f"is_raining = {is_raining}")

if not is_raining:
    print("No umbrella needed!")

# Complex conditions
print("\nComplex conditions:")
age = 30
income = 50000
print(f"age = {age}, income = {income}")

if age >= 21 and income >= 30000:
    print("You qualify for the premium credit card")

if age < 18 or income < 20000:
    print("You qualify for the student discount")

print("\n" + "=" * 50)
print("TERNARY OPERATOR (Conditional Expression)")
print("=" * 50)

x = 15
result = "Even" if x % 2 == 0 else "Odd"
print(f"\n{x} is {result}")

# Nested ternary (use sparingly for readability)
y = 10
result = "Positive" if y > 0 else ("Zero" if y == 0 else "Negative")
print(f"{y} is {result}")

print("\n" + "=" * 50)
print("PRACTICAL EXAMPLES")
print("=" * 50)

# Calculator
print("\nSimple Calculator:")
num1 = 15
num2 = 5
print(f"num1 = {num1}, num2 = {num2}")

print(f"Addition: {num1} + {num2} = {num1 + num2}")
print(f"Subtraction: {num1} - {num2} = {num1 - num2}")
print(f"Multiplication: {num1} * {num2} = {num1 * num2}")
print(f"Division: {num1} / {num2} = {num1 / num2}")
print(f"Integer Division: {num1} // {num2} = {num1 // num2}")
print(f"Modulus: {num1} % {num2} = {num1 % num2}")
print(f"Power: {num1} ** {num2} = {num1 ** num2}")

# Leap year check
print("\nLeap Year Check:")
year = 2024
print(f"year = {year}")

is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"Is {year} a leap year? {is_leap}")

if is_leap:
    print(f"{year} has 366 days")
else:
    print(f"{year} has 365 days")
