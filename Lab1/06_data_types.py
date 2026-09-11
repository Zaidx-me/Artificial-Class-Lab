# Lab 1: Data Types and Type Casting
# This program demonstrates Python's built-in data types

print("=" * 50)
print("NUMERIC TYPES")
print("=" * 50)

# Integer (int) - whole numbers
x = 10
y = -5
z = 0
print(f"Integer examples: {x}, {y}, {z}")
print(f"Type of {x}: {type(x)}")

# Float - decimal numbers
pi = 3.14159
temperature = -2.5
scientific = 1.5e10  # Scientific notation
print(f"\nFloat examples: {pi}, {temperature}, {scientific}")
print(f"Type of {pi}: {type(pi)}")

# Complex numbers
complex1 = 3 + 4j
complex2 = complex(2, 3)  # Using complex() constructor
print(f"\nComplex examples: {complex1}, {complex2}")
print(f"Real part of {complex1}: {complex1.real}")
print(f"Imaginary part of {complex1}: {complex1.imag}")

print("\n" + "=" * 50)
print("BOOLEAN TYPE")
print("=" * 50)

# Boolean (bool) - True or False
is_student = True
is_graduated = False
print(f"Boolean examples: {is_student}, {is_graduated}")
print(f"Type of {is_student}: {type(is_student)}")

# Booleans are actually integers
print(f"\nTrue + True = {True + True}")
print(f"True * 10 = {True * 10}")
print(f"False + 1 = {False + 1}")

# Boolean operations
a = True
b = False
print(f"\n{a} and {b} = {a and b}")
print(f"{a} or {b} = {a or b}")
print(f"not {a} = {not a}")

print("\n" + "=" * 50)
print("STRING TYPE")
print("=" * 50)

# String (str) - sequence of characters
name = "Python"
greeting = 'Hello, World!'
multi_line = """This is a
multi-line string"""
empty_string = ""

print(f"String examples:")
print(f"  name: {name}")
print(f"  greeting: {greeting}")
print(f"  multi_line: {multi_line}")
print(f"  empty_string: '{empty_string}'")

# Strings are immutable
text = "Hello"
# text[0] = "h"  # This would cause TypeError

# String operations
print(f"\nString operations:")
print(f"  Length of '{name}': {len(name)}")
print(f"  Uppercase: {name.upper()}")
print(f"  Lowercase: {name.lower()}")
print(f"  Reverse: {name[::-1]}")

# Escape sequences
print("\nEscape sequences:")
print("  Newline: Line1\nLine2")
print("  Tab: Column1\tColumn2")
print("  Backslash: C:\\Users\\Documents")
print("  Single quote: It\\'s a beautiful day")
print("  Double quote: He said \\\"Hello\\\"")

# String indexing
print("\nString indexing:")
word = "PYTHON"
print(f"  Word: {word}")
print(f"  First character: {word[0]}")
print(f"  Last character: {word[-1]}")
print(f"  Character at index 2: {word[2]}")

# String slicing
print("\nString slicing:")
print(f"  First 3 characters: {word[:3]}")
print(f"  Last 3 characters: {word[-3:]}")
print(f"  Characters from index 1 to 4: {word[1:5]}")

print("\n" + "=" * 50)
print("TYPE CASTING")
print("=" * 50)

# Type casting examples
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)

print(f"String '{num_str}' cast to int: {num_int}")
print(f"String '{num_str}' cast to float: {num_float}")

# Float to int (truncates, doesn't round)
pi_float = 3.14159
pi_int = int(pi_float)
print(f"\nFloat {pi_float} cast to int: {pi_int}")

# Int to string
age = 25
age_str = str(age)
print(f"\nInt {age} cast to string: '{age_str}'")

# Bool to int
print(f"\nTrue as int: {int(True)}")
print(f"False as int: {int(False)}")
