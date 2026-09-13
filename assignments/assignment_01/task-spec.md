# Benchmark Task: Student Grades Manager (Python)

This exact specification is given to every tool under test. Nothing changes between runs.

## Goal

Build a Python CLI program called `grades.py` in a fresh, empty project folder.

## Requirements

1. Read student records from a text file `students.txt`.
   - Format: one record per line → `Name,Mark1,Mark2,Mark3`
2. For each student compute:
   - **Average** mark (mean of the 3 marks)
   - **Highest** mark
   - **Letter grade** using: A ≥ 85, B ≥ 70, C ≥ 60, D ≥ 50, F < 50
3. Print a neatly formatted table: `Name | Average | Highest | Grade`
4. Print class statistics:
   - Overall average across all students
   - Name of the top scorer and the lowest scorer
5. Handle invalid lines gracefully (skip them and print a warning line).
6. Round averages to 2 decimal places.

## Files

- `grades.py` — main program
- `students.txt` — sample data (5+ students)
- `test_grades.py` — 3 unit tests using `pytest`

## Sample input (`students.txt`)

```
Ali,78,85,90
Sara,62,70,55
Hamza,92,88,95
Ayesha,45,50,48
Bilal,70,73,69
```

## Expected output

```
Name        Average   Highest   Grade
--------------------------------------
Ali         84.33     90        B
Sara        62.33     70        C
Hamza       91.67     95        A
Ayesha      47.67     50        F
Bilal       70.67     73        B

Class Stats:
Overall Average: 71.33
Top Scorer: Hamza (91.67)
Lowest Scorer: Ayesha (47.67)
```

> Bilal's grade is **B** (70.67 ≥ 70 threshold). Older drafts of the sample output
> wrongly showed "C" — the threshold rule above is authoritative.

## Acceptance checks

- [ ] `python3 grades.py` produces output matching the expected format
- [ ] `pytest test_grades.py` passes (3 tests)
- [ ] Rounded averages to 2 decimals
- [ ] Invalid lines are skipped with a warning