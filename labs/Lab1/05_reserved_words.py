# Lab 1: Python Reserved Words
# This program demonstrates Python's reserved keywords

# Python reserved words cannot be used as variable names
# Here are all Python 3.10+ reserved words:

reserved_words = [
    "False", "None", "True", "and", "as", "assert",
    "async", "await", "break", "class", "continue",
    "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in",
    "is", "lambda", "nonlocal", "not", "or", "pass",
    "raise", "return", "try", "while", "with", "yield"
]

print("Python Reserved Words:")
print("-" * 40)

# Display reserved words in a formatted way
for i, word in enumerate(reserved_words):
    print(f"{word:15}", end="")
    if (i + 1) % 5 == 0:  # New line every 5 words
        print()

print("\n")

# You can check if a word is reserved using keyword module
import keyword

test_words = ["for", "while", "my_var", "class", "function", "return"]
print("Testing if words are reserved:")
for word in test_words:
    is_reserved = keyword.iskeyword(word)
    print(f"{word:15} -> {'Reserved' if is_reserved else 'Not Reserved'}")

# Note: Trying to use reserved words as variable names causes SyntaxError
# Uncomment the following lines to see the error:
# for = 10      # SyntaxError
# class = "test" # SyntaxError
# True = 1       # SyntaxError
