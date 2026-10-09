# Artificial-Class-Lab

> Course repository — *Introduction to AI and Its Application Using Python*

Everything done in this course lives here, split into two top-level folders:
**labs** (hands-on Python exercises) and **assignments** (graded projects/studies).

| Folder | What lives here |
|--------|-----------------|
| [`labs/`](labs/) | In-class labs — each with its own `README.md` (explanation), `manual.md` (official sheet), and numbered `NN_topic.py` scripts |
| [`assignments/`](assignments/) | Assignments — each with its task spec, results, code, and report |

---

## Repository Layout

```
Artificial-Class-Lab/
│
├── README.md                 ← You are here (navigation hub)
│
├── labs/                     ← Labs
│   ├── Lab1/                 ← Lab 1: Python Fundamentals
│   │   ├── README.md         ← Explanatory guide → links to manual + all scripts
│   │   ├── manual.md         ← Lab 1 manual
│   │   └── 01_python_syntax.py … 11_common_in_two_arrays.py
│   ├── Lab2/                 ← Lab 2: Loops, Functions & Classes
│   │   ├── README.md         ← Explanatory guide → links to all scripts
│   │   └── 01_while_loop.py … 13_object_methods.py
│   ├── Lab3/                 ← Lab 3: Problem-Solving with Python
│   │   ├── README.md         ← Explanatory guide → links to manual + all scripts
│   │   ├── Lab 3.pdf         ← Lab 3 manual
│   │   └── 01_divisible_by_7_and_5.py … 16_password_strength_checker.py
│   ├── Lab4/                 ← Lab 4: Stacks, Queues & Binary Search
│   │   ├── README.md         ← Explanatory guide → links to manual + all scripts
│   │   ├── Lab 4.pdf         ← Lab 4 manual
│   │   └── 01_stack.py … 03_binary_search.py
│   └── Lab5/                 ← Lab 5: BFS & Priority Queue
│       ├── README.md         ← Explanatory guide → links to manual + all scripts
│       ├── Lab 5.pdf         ← Lab 5 manual
│       └── 01_bfs.py … 03_priority_queue.py
│
├── assignments/              ← Assignments
│   └── assignment_01/        ← Assignment 1: Benchmarking 10 AI Coding IDEs
│       ├── README.md         ← Study summary + navigation
│       ├── task-spec.md      ← the benchmark task
│       ├── results/          ← scoring data (scores, ranking, methodology, rubric, analysis)
│       ├── code/             ← produced code (live-run + reference implementations)
│       ├── tools/            ← one page per IDE (install + facts)
│       ├── report/           ← docs for the written report
│       └── implementation-plan.md
│
└── .gitignore
```

---

## Labs Index

| Lab | Topics | Explanation | Manual | Scripts | Status |
|-----|--------|-------------|--------|---------|--------|
| **Lab 1** | Python syntax, input/output, data types, strings, lists, conditionals | [Read](labs/Lab1/README.md) | [View](labs/Lab1/manual.md) | [Run](labs/Lab1/README.md#how-to-run) | Complete |
| **Lab 2** | `while`/`for` loops, `break`/`continue`, functions, classes & objects | [Read](labs/Lab2/README.md) | — | [Run](labs/Lab2/README.md#how-to-run) | Complete |
| **Lab 3** | Nested loops, data structures, strings, `random`, regex, 2D arrays | [Read](labs/Lab3/README.md) | [View](labs/Lab3/Lab%203.pdf) | [Run](labs/Lab3/README.md#how-to-run) | Complete |
| **Lab 4** | Stacks (LIFO), queues (FIFO), binary search | [Read](labs/Lab4/README.md) | [View](labs/Lab4/Lab%204.pdf) | [Run](labs/Lab4/README.md#how-to-run) | Complete |
| **Lab 5** | BFS (graphs & trees), early goal stopping, priority queue | [Read](labs/Lab5/README.md) | [View](labs/Lab5/Lab%205.pdf) | [Run](labs/Lab5/README.md#how-to-run) | Complete |
| **Lab 6** | *To be assigned* | — | — | — | Pending |

> **Pattern:** Every new lab folder follows the same structure — `README.md` (explanation), `manual.md` (manual), and numbered `NN_topic.py` scripts.

---

## Assignments Index

| Assignment | Topic | Entry point | Status |
|------------|-------|-------------|--------|
| **Assignment 1** | Benchmarking 10 modern AI coding IDEs on a single Python task | [assignments/assignment_01/README.md](assignments/assignment_01/README.md) | Complete (4 live runs, 5 simulated, 1 estimated) |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Zaidx-me/Artificial-Class-Lab.git
cd Artificial-Class-Lab
```

### 2. Run any lab script

```bash
cd labs/Lab1
python3 01_python_syntax.py
python3 07_lists.py
# ... etc
```

> **Note:** Scripts with user input (e.g. `02_input_output.py`) require interactive input when run.

### 3. Run the assignment tests

```bash
cd assignments/assignment_01/code/live-run/trae
python3 -m pytest
```

### 4. Requirements

- **Python 3.6+** (scripts use f-strings)
- **No external packages** — Python standard library only (pytest for the assignment tests)

---

## Repository Conventions

- Each lab folder is self-contained: **explanation** + **manual** + **scripts**
- Each assignment folder is self-contained: **task** + **results** + **code** + **report**
- Scripts are numbered (`NN_topic.py`) to reflect the order topics are introduced
- Code follows the **PEP 8** conventions taught in Lab 1 (4-space indentation, 79-char lines)
- Python artifacts and agent metadata are excluded via `.gitignore`