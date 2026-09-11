# Lab 1 — Introduction to AI and Its Application Using Python

> The official lab manual / reference guide for Lab 1.
> Correlating scripts: [`README.md`](README.md) explains each file in detail.

---

## 1. Why Python for AI?

Python is widely used for artificial intelligence, with packages for a number of applications including **General AI**, **Machine Learning**, **Natural Language Processing**, and **Neural Networks**. *(Haskell is also a very good programming language for AI.)*

Python is a general-purpose **interpreted, interactive, object-oriented, and high-level** programming language. It was created by **Guido van Rossum** during 1985–1990. Like Perl, Python source code is also available under the GNU General Public License (GPL).

| Feature | Description |
|---------|-------------|
| **Interpreted** | Processed at runtime by the interpreter — no compilation step needed (similar to PERL and PHP) |
| **Interactive** | You can sit at a Python prompt and interact with the interpreter directly to write programs |
| **Object-Oriented** | Supports OOP style/technique that encapsulates code within objects |
| **Beginner-Friendly** | Great for beginners; supports everything from text processing to WWW browsers to games |

---

## 2. Programming Syntax

### 2.1 Executing Python Syntax

Python syntax can be executed in two ways:

1. **Directly in the Command Line** (interactive prompt):
   ```python
   >>> print("Hello, World!")
   Hello, World!
   ```

2. **By creating a Python file** (`.py` extension) and running it in the Command Line:
   ```
   C:\Users\Your Name>python myfile.py
   ```

A Python program is read by a parser. Python was designed to be a highly readable language. The syntax of the Python programming language is the set of rules which defines how a Python program will be written.

### 2.2 Comments in Python

A comment begins with a hash character (`#`) which is *not* part of the string literal and ends at the end of the physical line. All characters after the `#` character up to the end of the line are part of the comment and the Python interpreter ignores them.

```python
# This is a comment — ignored by the interpreter
print("Hello, World!")  # inline comment
```

> **Note:** Python has **no multi-line or block comments** facility — each comment line needs its own `#`.

### 2.3 Input / Output

```python
txt = input("Type something to test this out: ")
print(txt)
```

### 2.4 Multiple Statements on a Single Line

You can write two separate statements into a single line using a **semicolon (`;`)** character between them:

```python
a = 10; b = 20; print(a + b)
```

### 2.5 Indentation

Python uses whitespace (spaces and tabs) to define program blocks, whereas other languages like C and C++ use braces (`{}`). The number of whitespaces in the indentation is **not fixed**, but all statements within the block **must be indented the same amount**.

```python
if True:
    print("Inside the block")   # indented statement
```

Indentation levels can vary across programs: no indentation, single-space, single-tab, or a single space + single tab — what matters is consistency within each block.

---

## 3. Python Coding Style

- Use **4 spaces** per indentation and **no tabs**.
- **Do not mix tabs and spaces** — tabs create confusion; only spaces are recommended.
- **Maximum line length: 79 characters**, which helps users with a small display.
- Use blank lines to separate top-level function and class definitions, and a single blank line to separate method definitions inside a class and larger blocks of code inside functions.
- When possible, put inline comments (should be complete sentences).
- Use spaces around expressions and statements.

---

## 4. Python Reserved Words

The following identifiers are used as **reserved words** of the language and **cannot be used as ordinary identifiers** (variable names, function names, etc.):

```
False   None    True    and     as      assert
async   await   break   class   continue
def     del     elif    else    except  finally
for     from    global  if      import  in
is      lambda  nonlocal not     or      pass
raise   return  try     while   with    yield
```

---

## 5. Data Types and Type Casting

A **type** represents the kind of value and determines how the value can be used. All data values in Python are encapsulated in relevant object classes. Everything in Python is an object, and every object has an **identity**, a **type**, and a **value**.

To determine a variable's type in Python, use the `type()` function:

```python
>>> type(10)
<class 'int'>
```

Objects whose value can be changed are called **mutable**; objects whose value is unchangeable (once created) are called **immutable**.

### 5.1 Numbers

Numbers are created by numeric literals. **Numeric objects are immutable** — once created, their value cannot be changed.

Python has three distinct numeric types:

| Type | Description | Example |
|------|-------------|---------|
| `int` | Integers — negative/positive whole numbers without fractional parts | `10`, `-5`, `0` |
| `float` | Floating point — negative/positive numbers with fractional parts | `3.14`, `-2.5` |
| `complex` | Complex numbers (engineering) of the form **A + Bi** | `3 + 4j` |

**Booleans are a subtype of plain integers.**

Complex numbers have a **real** and an **imaginary** part. Python supports them either in `(real + imagJ)` / `(real + imagj)` form or via the built-in `complex(x, y)` method:

```python
>>> z = 3 + 4j
>>> z.real
3.0
>>> z.imag
4.0
>>> c = complex(2, 3)
(2+3j)
```

### 5.2 Boolean (`bool`)

The simplest built-in type in Python is the **`bool`** type. It represents the truth values `False` and `True`.

```python
>>> a = True
>>> b = False
>>> a and b
False
>>> a or b
True
>>> not a
False
```

### 5.3 Strings

A string type object is a **sequence** (left-to-right order) of **characters**. Strings start and end with single or double quotes. **Python strings are immutable.**

- Single and double quoted strings are the same.
- You can use a single quote within a string when it is surrounded by double quotes, and vice versa.

```python
>>> name = "Python"
>>> greeting = 'Hello'
>>> quote = "It's a beautiful day"
```

#### 5.3.1 Special Characters in Strings

The backslash (`\`) character is used to introduce a special character:

| Escape Sequence | Meaning |
|-----------------|---------|
| `\n` | Newline |
| `\t` | Horizontal Tab |
| `\\` | Backslash |
| `\'` | Single Quote |
| `\"` | Double Quote |

**Example:**
```python
>>> print("Line1\nLine2")
Line1
Line2
>>> print("Tab:\tColumn2")
Tab:	Column2
```

#### 5.3.2 String Indices and Accessing String Elements

Strings are arrays of characters, and elements can be accessed using **indexing**:
- Indices start with **0** from the left side
- Indices start with **-1** when starting from the right side

```python
string1 = "PYTHON TUTORIAL"
```

| Character | P | Y | T | H | O | N |   | T | U | T | O | R | I | A | L |
|-----------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Index (from left) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| Index (from right) | -15 | -14 | -13 | -12 | -11 | -10 | -9 | -8 | -7 | -6 | -5 | -4 | -3 | -2 | -1 |

```python
>>> string1[0]
'P'
>>> string1[7]
'T'
>>> string1[-1]
'L'
>>> string1[-15]
'P'
```

#### 5.3.3 String Slicing

To cut a substring from a string is called **string slicing**. Two indices are used, separated by a colon (`:`).

- A slice `3:7` means characters at indices 3, 4, 5, and 6 — the **second index (7) is not included**.
- Negative indices can be used for slicing too.

```python
>>> string1 = "PYTHON TUTORIAL"
>>> string1[3:7]
'HON '
>>> string1[:6]
'PYTHON'
>>> string1[-7:]
'TUTORIAL'
```

---

## 6. Lists

A list is a container which holds **comma-separated values** (items or elements) between **square brackets**. Items or elements need **not all have the same type**.

### 6.1 Creating Lists

```python
empty_list = []                              # empty list
numbers = [1, 2, 3, 4, 5]
mixed = [1, "Hello", 3.14, True]             # mixed types allowed
nested = [[1, 2], [3, 4]]                    # nested lists
```

### 6.2 List Indices

List indices work the same way as string indices — they start at **0**. Positive values count from the beginning; negative values count backward from the end.

```python
color_list = ["RED", "Blue", "Green", "Black"]
```

| Item | RED | Blue | Green | Black |
|------|-----|------|-------|-------|
| Index (from left) | 0 | 1 | 2 | 3 |
| Index (from right) | -4 | -3 | -2 | -1 |

```python
>>> color_list[0]
'RED'
>>> color_list[3]
'Black'
>>> color_list[-1]
'Black'
>>> color_list[-4]
'RED'
```

> **Caution:** Giving an index value which is **out of range** makes the interpreter raise an error message:
> ```python
> >>> color_list[5]
> IndexError: list index out of range
> ```

### 6.3 List Slicing

Lists can be sliced like strings and other sequences. The syntax of list slices is:

```
sliced_list = List_Name[startIndex:endIndex]
```

```python
>>> color_list[1:3]
['Blue', 'Green']
>>> color_list[:2]
['RED', 'Blue']
>>> color_list[-2:]
['Green', 'Black']
```

---

## 7. Conditional Statements

Python supports the usual logical conditions from mathematics:

| Operator | Meaning |
|----------|---------|
| `==` | Equals |
| `!=` | Not Equals |
| `<` | Less than |
| `<=` | Less than or equal to |
| `>` | Greater than |
| `>=` | Greater than or equal to |

**Example:**

```python
b = 20
a = 10

if b > a:
    print("b is greater than a")
```

---

## Summary of Demo Scripts

| Script | Covers |
|--------|--------|
| `01_python_syntax.py` | §2.1–2.2 — syntax & comments |
| `02_input_output.py` | §2.3 — input/output |
| `03_multiple_statements.py` | §2.4 — semicolons |
| `04_indentation.py` | §2.5 — indentation |
| `05_reserved_words.py` | §4 — reserved words |
| `06_data_types.py` | §5 — data types & casting |
| `07_lists.py` | §6 — lists |
| `08_conditionals.py` | §7 — conditional statements |