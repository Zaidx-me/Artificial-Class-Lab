# Lab 3 — Problem-Solving with Python

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 3.pdf](Lab%203.pdf) — the original assignment sheet |

---

## Overview

Lab 3 is a set of short programming problems (`01_divisible_by_7_and_5.py` … `16_password_strength_checker.py`) that put the
Lab 1–2 fundamentals to work: nested loops, control flow, sequences, sets and
dictionaries, string handling, `random`, and even a first taste of regular
expressions (`re`). Each question is an independent script — run it and follow
the prompts.

## Files in This Lab

| # | File | Problem |
|---|------|---------|
| 01 | [`01_divisible_by_7_and_5.py`](01_divisible_by_7_and_5.py) | Numbers divisible by 7 and multiples of 5 (1500–2700) |
| 02 | [`02_temperature_conversion.py`](02_temperature_conversion.py) | Temperature conversion: Celsius ↔ Fahrenheit |
| 03 | [`03_guess_the_number.py`](03_guess_the_number.py) | Guess-the-number game (1–9) with `random` |
| 04 | [`04_star_pattern.py`](04_star_pattern.py) | Star pattern (diamond) with nested loops |
| 05 | [`05_reverse_word.py`](05_reverse_word.py) | Reverse a word character by character |
| 06 | [`06_count_even_odd.py`](06_count_even_odd.py) | Count even and odd numbers in a tuple |
| 07 | [`07_item_and_type.py`](07_item_and_type.py) | Print items and their types from a mixed list |
| 08 | [`08_skip_3_and_6.py`](08_skip_3_and_6.py) | Loop control: skip 3 and 6 with `continue` |
| 09 | [`09_fibonacci_series.py`](09_fibonacci_series.py) | Fibonacci series up to 50 with a `while` loop |
| 10 | [`10_fizzbuzz.py`](10_fizzbuzz.py) | FizzBuzz from 1 to 50 |
| 11 | [`11_2d_array_ij_values.py`](11_2d_array_ij_values.py) | 2D array (matrix) filled with `i * j` values |
| 12 | [`12_lines_to_lowercase.py`](12_lines_to_lowercase.py) | Read lines until blank, print them lowercase |
| 13 | [`13_binary_divisible_by_5.py`](13_binary_divisible_by_5.py) | Pick comma-separated 4-digit binaries divisible by 5 |
| 14 | [`14_count_letters_digits.py`](14_count_letters_digits.py) | Count letters and digits in a string |
| 15 | [`15_password_validity_regex.py`](15_password_validity_regex.py) | Password validity checker using regex (`re`) |
| 16 | [`16_password_strength_checker.py`](16_password_strength_checker.py) | Password strength checker with character classification |

---

## Detailed File Guide

### 01_divisible_by_7_and_5.py — Divisible by 7 and Multiple of 5

Collects every number between 1500 and 2700 that is divisible by both 7 and 5.

**Concepts demonstrated:**
- `range(1500, 2701)` iteration
- Combining conditions with `and` (`num % 7 == 0 and num % 5 == 0`)
- Accumulating results with `append()`

---

### 02_temperature_conversion.py — Temperature Conversion

Converts fixed sample values between Celsius and Fahrenheit.

**Concepts demonstrated:**
- The conversion formulas `(9 * c / 5) + 32` and `5 * (f - 32) / 9`
- `int()` to round the result
- f-strings / formatted output with `°C` and `°F` labels

---

### 03_guess_the_number.py — Guess a Number (1 to 9)

Picks a random target and loops until the player guesses it.

**Concepts demonstrated:**
- `import random` and `random.randint(1, 9)`
- An infinite `while True:` loop terminated by `break`
- Comparing `input()` cast with `int()` against the target

---

### 04_star_pattern.py — Star Pattern (Nested Loop)

Prints a symmetric star diamond using two nested loops.

**Concepts demonstrated:**
- Inner loop runs `i` times to place the stars
- `print("*", end=" ")` builds a row without a newline; a bare `print()`
  moves to the next line
- A decreasing `range(n - 1, 0, -1)` loop for the lower half

---

### 05_reverse_word.py — Reverse a Word

Builds the reversed word by prepending each character.

**Concepts demonstrated:**
- Prepending: `reversed_word = char + reversed_word`
- String concatenation in a `for` loop

---

### 06_count_even_odd.py — Count Even and Odd Numbers

Counts evens and odds inside a tuple of numbers.

**Concepts demonstrated:**
- Iterating over a tuple
- `num % 2 == 0` parity test with `if`/`else` counters

---

### 07_item_and_type.py — Print Item and Type from List

Walks a list holding many different data types and prints each with its type.

**Concepts demonstrated:**
- A mixed-type list: int, float, complex, bool, str, tuple, list, dict, set
- The built-in `type()` function
- f-strings: `f"Item: {item}, Type: {type(item)}"`

---

### 08_skip_3_and_6.py — Loop Control with `continue`

Prints the numbers 0–6, skipping 3 and 6.

**Concepts demonstrated:**
- `continue` skipping specific iterations
- `print(num, end=" ")` for a single-line output

**Example output:**
```
0 1 2 4 5
```

---

### 09_fibonacci_series.py — Fibonacci Series (`while` loop)

Prints Fibonacci numbers while they stay below 50.

**Concepts demonstrated:**
- Tuple unpacking swap: `a, b = b, a + b`
- A `while b < 50:` loop

---

### 10_fizzbuzz.py — FizzBuzz (1 to 50)

The classic FizzBuzz problem over 1–50.

**Concepts demonstrated:**
- `% 3 == 0 and % 5 == 0` checks in priority order (`if`/`elif`/`else`)
- Printing "FizzBuzz", "Fizz", "Buzz" or the number itself

---

### 11_2d_array_ij_values.py — 2D Array with `i * j` Values

Builds an `m × n` matrix where cell `(i, j)` holds `i * j`.

**Concepts demonstrated:**
- Nested loops with `range(m)` / `range(n)`
- Building rows with `append()` and pushing them into the outer list
- Reading matrix dimensions with `input()` and `int()`

---

### 12_lines_to_lowercase.py — Lines to Lowercase (Blank Line Terminates)

Reads lines from the user until an empty line, then prints them in lowercase.

**Concepts demonstrated:**
- `while True:` with `break` on `line == ""`
- `str.lower()` on each stored line
- A `lines` list that is re-printed afterwards

---

### 13_binary_divisible_by_5.py — 4-Digit Binary Numbers Divisible by 5

Filters a comma-separated list of binary numbers by divisibility by 5.

**Concepts demonstrated:**
- `input().split(',')` to parse comma-separated values
- `int(b, 2)` — base-2 (binary) conversion
- `",".join(...)` to rebuild the output string

---

### 14_count_letters_digits.py — Count Letters and Digits

Counts alphabetic and numeric characters in a string.

**Concepts demonstrated:**
- `str.isalpha()` and `str.isdigit()` tests
- Branching with `if`/`elif` and running counters

---

### 15_password_validity_regex.py — Password Validity Checker

Validates a password with the rules: 6–16 characters, at least one lowercase,
one uppercase, one digit, and one of `$ # @`.

**Concepts demonstrated:**
- `import re` and `re.search("[a-z]", ...)` patterns
- Chained `if`/`elif` validation with an `is_valid` flag
- A common real-world specification problem

---

### 16_password_strength_checker.py — Password Strength Checker (no regex)

A second take on the same password rules using character classification
instead of regular expressions.

**Concepts demonstrated:**
- Boolean flags (`has_lower`, `has_upper`, `has_digit`) and a
  `special_count` counter
- `str.islower()`, `str.isupper()`, `str.isdigit()` per character
- A length check (`6 <= len(password) <= 16`) before the flag test

---

## How to Run

Each question is independent — run any of them with:

```bash
cd Lab3
python3 01_divisible_by_7_and_5.py
python3 13_binary_divisible_by_5.py
# ... etc
```

> **Note:** Most scripts (03, 05, 11–16) require
> interactive input when run.

**Requirements:** Python 3.6+ · standard library only (plus `random` and `re`,
which ship with Python)

---

## Manual Reference

The official lab manual for this lab: [`Lab 3.pdf`](Lab%203.pdf)

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |