# Artificial-Class-Lab

> Hands-on Python labs — *Introduction to AI and Its Application Using Python*

This repository contains a series of lab exercises on Python fundamentals. Each lab lives in its own folder with **three things**:

| What | File | Purpose |
|------|------|---------|
| **Explanation** | `README.md` | Independent, detailed guide to every file and concept in that lab |
| **Manual** | `manual.md` | The official lab manual / assignment sheet for the lab |
| **Scripts** | `*.py` | Runnable demonstration scripts per topic |

---

## Navigating This Repository

```
Artificial-Class-Lab/
│
├── README.md                ← You are here (navigation hub)
│
├── Lab1/                    ← Lab 1: Python Fundamentals
│   ├── README.md            ← Explanatory guide → links to manual + all scripts
│   ├── manual.md            ← Lab 1 manual
│   ├── 01_python_syntax.py
│   ├── 02_input_output.py
│   ├── 03_multiple_statements.py
│   ├── 04_indentation.py
│   ├── 05_reserved_words.py
│   ├── 06_data_types.py
│   ├── 07_lists.py
│   └── 08_conditionals.py
│
├── Lab2/                    ← Lab 2: (pending)   [coming soon]
├── Lab3/                    ← Lab 3: (pending)   [coming soon]
├── Lab4/                    ← Lab 4: (pending)   [coming soon]
│
└── .gitignore
```

**How to navigate:**

1. **Find your lab** → use the Labs table below
2. **Open the lab's `README.md`** → it explains every file in that lab, topic by topic
3. **Check the `manual.md`** → for the official assignment content
4. **Run the scripts** → each `.py` file is self-contained (see [Getting Started](#getting-started))

---

## Labs Index

| Lab | Topics | Explanation | Manual | Scripts | Status |
|-----|--------|-------------|--------|---------|--------|
| **Lab 1** | Python syntax, input/output, data types, strings, lists, conditionals | [Read](Lab1/README.md) | [View](Lab1/manual.md) | [Run](Lab1/README.md#how-to-run) | Complete |
| **Lab 2** | *To be assigned* | — | — | — | Pending |
| **Lab 3** | *To be assigned* | — | — | — | Pending |
| **Lab 4** | *To be assigned* | — | — | — | Pending |

> **Pattern:** Every new lab folder will follow the same structure — `README.md` (explanation), `manual.md` (manual), and numbered `NN_topic.py` scripts.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Zaidx-me/Artificial-Class-Lab.git
cd Artificial-Class-Lab
```

### 2. Run any lab script

```bash
cd Lab1
python3 01_python_syntax.py
python3 07_lists.py
# ... etc
```

> **Note:** Scripts with user input (e.g. `02_input_output.py`) require interactive input when run.

### 3. Requirements

- **Python 3.6+** (scripts use f-strings)
- **No external packages** — Python standard library only

---

## Repository Conventions

- Each lab folder is self-contained: **explanation** + **manual** + **scripts**
- Scripts are numbered (`NN_topic.py`) to reflect the order topics are introduced
- Code follows the **PEP 8** conventions taught in Lab 1 (4-space indentation, 79-char lines)
- Python artifacts and agent metadata are excluded via `.gitignore`