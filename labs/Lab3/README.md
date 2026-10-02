# Lab 3 — Problem-Solving with Python

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |
| **Official manual** | [Lab 3.pdf](Lab%203.pdf) — the original assignment sheet |

---

## Overview

Lab 3 is a set of short programming problems (`q1.py` … `q14_2.py`) that put the
Lab 1–2 fundamentals to work: nested loops, control flow, sequences, sets and
dictionaries, string handling, `random`, and even a first taste of regular
expressions (`re`). Each question is an independent script — run it and follow
the prompts.

## Files in This Lab

| # | File | Problem |
|---|------|---------|
| 01 | [`q1.py`](q1.py) | Numbers divisible by 7 and multiples of 5 (1500–2700) |
| 02 | [`q2.py`](q2.py) | Temperature conversion: Celsius ↔ Fahrenheit |
| 03 | [`q3.py`](q3.py) | Guess-the-number game (1–9) with `random` |
| 04 | [`q4.py`](q4.py) | Star pattern (diamond) with nested loops |
| 05 | [`q5.py`](q5.py) | Reverse a word character by character |
| 06 | [`q6.py`](q6.py) | Count even and odd numbers in a tuple |
| 07 | [`q7.py`](q7.py) | Print items and their types from a mixed list |
| 08 | [`q8.py`](q8.py) | Loop control: skip 3 and 6 with `continue` |
| 09 | [`q9_a.py`](q9_a.py) | Fibonacci series up to 50 with a `while` loop |
| 10 | [`q9_b.py`](q9_b.py) | FizzBuzz from 1 to 50 |
| 11 | [`q10.py`](q10.py) | 2D array (matrix) filled with `i * j` values |
| 12 | [`q11.py`](q11.py) | Read lines until blank, print them lowercase |
| 13 | [`q12.py`](q12.py) | Pick comma-separated 4-digit binaries divisible by 5 |
| 14 | [`q13.py`](q13.py) | Count letters and digits in a string |
| 15 | [`q14.py`](q14.py) | Password validity checker using regex (`re`) |
| 16 | [`q14_2.py`](q14_2.py) | Password strength checker with character classification |

---

## Detailed File Guide

### q1.py — Divisible by 7 and Multiple of 5

Collects every number between 1500 and 2700 that is divisible by both 7 and 5.

**Concepts demonstrated:**
- `range(1500, 2701)` iteration
- Combining conditions with `and` (`num % 7 == 0 and num % 5 == 0`)
- Accumulating results with `append()`

---

### q2.py — Temperature Conversion

Converts fixed sample values between Celsius and Fahrenheit.

**Concepts demonstrated:**
- The conversion formulas `(9 * c / 5) + 32` and `5 * (f - 32) / 9`
- `int()` to round the result
- f-strings / formatted output with `°C` and `°F` labels

---

### q3.py — Guess a Number (1 to 9)

Picks a random target and loops until the player guesses it.

**Concepts demonstrated:**
- `import random` and `random.randint(1, 9)`
- An infinite `while True:` loop terminated by `break`
- Comparing `input()` cast with `int()` against the target

---

### q4.py — Star Pattern (Nested Loop)

Prints a symmetric star diamond using two nested loops.

**Concepts demonstrated:**
- Inner loop runs `i` times to place the stars
- `print("*", end=" ")` builds a row without a newline; a bare `print()`
  moves to the next line
- A decreasing `range(n - 1, 0, -1)` loop for the lower half

---

### q5.py — Reverse a Word

Builds the reversed word by prepending each character.

**Concepts demonstrated:**
- Prepending: `reversed_word = char + reversed_word`
- String concatenation in a `for` loop

---

### q6.py — Count Even and Odd Numbers

Counts evens and odds inside a tuple of numbers.

**Concepts demonstrated:**
- Iterating over a tuple
- `num % 2 == 0` parity test with `if`/`else` counters

---

### q7.py — Print Item and Type from List

Walks a list holding many different data types and prints each with its type.

**Concepts demonstrated:**
- A mixed-type list: int, float, complex, bool, str, tuple, list, dict, set
- The built-in `type()` function
- f-strings: `f"Item: {item}, Type: {type(item)}"`

---

### q8.py — Loop Control with `continue`

Prints the numbers 0–6, skipping 3 and 6.

**Concepts demonstrated:**
- `continue` skipping specific iterations
- `print(num, end=" ")` for a single-line output

**Example output:**
```
0 1 2 4 5
```

---

### q9_a.py — Fibonacci Series (`while` loop)

Prints Fibonacci numbers while they stay below 50.

**Concepts demonstrated:**
- Tuple unpacking swap: `a, b = b, a + b`
- A `while b < 50:` loop

---

### q9_b.py — FizzBuzz (1 to 50)

The classic FizzBuzz problem over 1–50.

**Concepts demonstrated:**
- `% 3 == 0 and % 5 == 0` checks in priority order (`if`/`elif`/`else`)
- Printing "FizzBuzz", "Fizz", "Buzz" or the number itself

---

### q10.py — 2D Array with `i * j` Values

Builds an `m × n` matrix where cell `(i, j)` holds `i * j`.

**Concepts demonstrated:**
- Nested loops with `range(m)` / `range(n)`
- Building rows with `append()` and pushing them into the outer list
- Reading matrix dimensions with `input()` and `int()`

---

### q11.py — Lines to Lowercase (Blank Line Terminates)

Reads lines from the user until an empty line, then prints them in lowercase.

**Concepts demonstrated:**
- `while True:` with `break` on `line == ""`
- `str.lower()` on each stored line
- A `lines` list that is re-printed afterwards

---

### q12.py — 4-Digit Binary Numbers Divisible by 5

Filters a comma-separated list of binary numbers by divisibility by 5.

**Concepts demonstrated:**
- `input().split(',')` to parse comma-separated values
- `int(b, 2)` — base-2 (binary) conversion
- `",".join(...)` to rebuild the output string

---

### q13.py — Count Letters and Digits

Counts alphabetic and numeric characters in a string.

**Concepts demonstrated:**
- `str.isalpha()` and `str.isdigit()` tests
- Branching with `if`/`elif` and running counters

---

### q14.py — Password Validity Checker

Validates a password with the rules: 6–16 characters, at least one lowercase,
one uppercase, one digit, and one of `$ # @`.

**Concepts demonstrated:**
- `import re` and `re.search("[a-z]", ...)` patterns
- Chained `if`/`elif` validation with an `is_valid` flag
- A common real-world specification problem

---

### q14_2.py — Password Strength Checker (no regex)

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
python3 q1.py
python3 q12.py
# ... etc
```

> **Note:** Most scripts (q3, q5, q10, q11, q12, q13, q14, q14_2) require
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