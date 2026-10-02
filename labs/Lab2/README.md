# Lab 2 — Loops, Functions & Classes

> **Introduction to AI and Its Application Using Python**

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |

---

## Overview

Lab 2 continues where Lab 1 left off, covering Python's control-flow and
reusable-code building blocks: `while` and `for` loops, loop-control statements
(`break` / `continue`), functions (definition, parameters, default values,
return values, keyword arguments) and an introduction to classes and objects.
Each topic below has its own runnable script, listed in teaching order.

## Files in This Lab

| # | File | Topic |
|---|------|-------|
| 01 | [`01_while_loop.py`](01_while_loop.py) | `while` loop with a counter |
| 02 | [`02_while_single_statement copy.py`](02_while_single_statement%20copy.py) | `while` loop with a single-statement body |
| 03 | [`03_iterating_over_list.py`](03_iterating_over_list.py) | `for` loop over list, tuple & string |
| 04 | [`04_iterating_index.py`](04_iterating_index.py) | `for` loop by index; `continue` & `break` |
| 05 | [`05_function.py`](05_function.py) | Defining & calling a function |
| 06 | [`06_function_parameter.py`](06_function_parameter.py) | Function parameters |
| 07 | [`07_default_parameter.py`](07_default_parameter.py) | Default parameter values |
| 08 | [`08_pass_list_parameter.py`](08_pass_list_parameter.py) | Passing a list to a function |
| 09 | [`09_return_value_function.py`](09_return_value_function.py) | Returning a value from a function |
| 10 | [`10_key_values.py`](10_key_values.py) | Keyword arguments (key-value pairs) |
| 11 | [`11_classes_objects.py`](11_classes_objects.py) | Creating a class & an object |
| 12 | [`12_init_function.py`](12_init_function.py) | The `__init__()` constructor |
| 13 | [`13_object_methods.py`](13_object_methods.py) | Methods on objects |

---

## Detailed File Guide

### 01_while_loop.py — While Loop with a Counter

Repeats a block as long as its condition stays true.

**Concepts demonstrated:**
- `while` loop syntax with a parenthesized condition
- Updating a counter variable (`count = count + 1`) to make progress
- The loop ends when the condition (`count < 3`) becomes false

**Example output:**
```
Hello Geek
Hello Geek
Hello Geek
```

---

### 02_while_single_statement copy.py — Single-Statement While Body

Shows that a `while` loop body may be a single statement on the same line.

**Concepts demonstrated:**
- `while (count == 0): print("Hello Geek")` — one-line loop body
- The loop runs while the count stays `0`

**Note:** A `while` loop whose condition never changes never terminates —
update the condition inside the loop for real programs.

---

### 03_iterating_over_list.py — For Loop Over Sequence Types

Iterates over the members of the three main sequence types.

**Concepts demonstrated:**
- `for i in l:` looping directly over a **list**
- Looping over a **tuple**
- Looping over a **string** (character by character)
- `print()` with an empty string (`"\n"`) to insert blank lines

---

### 04_iterating_index.py — Looping by Index & Loop Control

Iterates using the index, then introduces the two loop-control statements.

**Concepts demonstrated:**
- `for index in range(len(list)):` — index-based iteration
- `continue` — skips the rest of the current iteration (`"e"` and `"s"`
  are skipped, all other letters are printed)
- `break` — exits the loop entirely at the first `"e"` or `"s"`

---

### 05_function.py — Defining & Calling a Function

The minimal function lifecycle: define, then call.

**Concepts demonstrated:**
- A function with no parameters: `def my_function():`
- Calling it later by name: `my_function()`
- Code inside a function runs only when called

---

### 06_function_parameter.py — Function Parameters

Passes data into a function through a parameter.

**Concepts demonstrated:**
- One parameter: `def my_function(fname):`
- Using the parameter inside the body (`fname + " Refsnes"`)
- Calling the same function with different arguments

**Example output:**
```
Emil Refsnes
Tobias Refsnes
Linus Refsnes
```

---

### 07_default_parameter.py — Default Parameter Values

A parameter can have a fallback value used when the caller passes nothing.

**Concepts demonstrated:**
- Default value in the signature: `def my_function(country = "Norway")`
- Passing an argument overrides the default (`"Sweden"`, `"Pakistan"`, `"Brazil"`)
- Calling with no argument uses the default (`"Norway"`)

---

### 08_pass_list_parameter.py — Passing a List to a Function

A function can accept a collection and iterate over it.

**Concepts demonstrated:**
- A parameter that holds a list: `def my_function(food):`
- `for x in food:` to process each element
- Passing a fruits list and printing each item

---

### 09_return_value_function.py — Returning a Value

Functions can send data back to the caller with `return`.

**Concepts demonstrated:**
- `return 5*x` computes a result without printing it
- Using the returned value inside `print()`

**Example output:**
```
20
15
10
```

---

### 10_key_values.py — Keyword Arguments

Arguments can be passed by name, as key-value pairs.

**Concepts demonstrated:**
- Keyword arguments: `my_function(child1="Emil", child2="Tobias", child3="Linus")`
- Order does not matter when using keyword arguments
- The function reads each value by its parameter name

---

### 11_classes_objects.py — Creating a Class & an Object

The first step into object-oriented programming.

**Concepts demonstrated:**
- Class definition: `class MyClass: x = 5`
- Creating an object: `p1 = MyClass()`
- Accessing an attribute through the object: `p1.x`

---

### 12_init_function.py — The `__init__()` Constructor

The `__init__` method runs automatically when an object is created.

**Concepts demonstrated:**
- `def __init__(self, name, age):` — constructor with parameters
- Storing values on the object with `self.name` / `self.age`
- Creating an object: `p1 = Person("John", 36)`
- Reading the object's attributes: `p1.name`, `p1.age`

---

### 13_object_methods.py — Methods on Objects

Combines the constructor with a method that uses the object's own data.

**Concepts demonstrated:**
- `__init__` storing `self.name` and `self.age`
- A method (`myfunc`) that reads `self.name` and prints a message
- Calling a method on an object: `p1.myfunc()`

**Example output:**
```
Hello my name is John
```

---

## How to Run

Each script is independent — run any of them with:

```bash
cd Lab2
python3 01_while_loop.py
python3 04_iterating_index.py
# ... etc
```

**Requirements:** Python 3.6+ · no external packages

---

| Navigation | |
|---|---|
| **Repository hub** | [← Back to main README](../../README.md) |