#!/usr/bin/env python3
"""grades.py - Student Grades Manager

Reads student records from a text file (default: students.txt), where each
line has the format ``Name,Mark1,Mark2,Mark3``. For every student it computes
the average mark, the highest mark and a letter grade, then prints a neatly
formatted table followed by class-wide statistics.

Letter grade thresholds (based on the average mark):
    A >= 85
    B >= 70
    C >= 60
    D >= 50
    F < 50
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Student:
    name: str
    marks: List[float] = field(default_factory=list)

    @property
    def average(self) -> float:
        """Mean of the student's marks, rounded to 2 decimal places."""
        return round(sum(self.marks) / len(self.marks), 2)

    @property
    def highest(self) -> float:
        """Highest mark achieved by the student."""
        return max(self.marks)

    @property
    def grade(self) -> str:
        """Letter grade derived from the student's average mark."""
        return letter_grade(self.average)


def letter_grade(average: float) -> str:
    """Return the letter grade for a given average mark."""
    if average >= 85:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"


def parse_line(line: str) -> Optional[Student]:
    """Parse a single ``Name,Mark1,Mark2,Mark3`` line.

    Returns a :class:`Student` instance, or ``None`` if the line is invalid
    (wrong number of fields, empty name, or non-numeric marks).
    """
    line = line.strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 4:
        return None

    name = parts[0]
    if not name:
        return None

    try:
        marks = [float(p) for p in parts[1:]]
    except ValueError:
        return None

    return Student(name=name, marks=marks)


def load_students(filename: str) -> List[Student]:
    """Read students from ``filename``, skipping invalid lines with a warning."""
    students: List[Student] = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Warning: file '{filename}' not found.")
        return students

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        student = parse_line(raw_line)
        if student is None:
            print(f"Warning: skipping invalid line {line_number}: {raw_line.strip()!r}")
            continue
        students.append(student)

    return students


def _format_mark(value: float) -> str:
    """Format a mark without a trailing '.0' for whole numbers."""
    if value == int(value):
        return str(int(value))
    return str(value)


def print_table(students: List[Student]) -> None:
    """Print the 'Name | Average | Highest | Grade' table."""
    print(f"{'Name':<12}{'Average':<10}{'Highest':<10}{'Grade':<6}")
    print("-" * 40)
    for student in students:
        print(
            f"{student.name:<12}{student.average:<10.2f}"
            f"{_format_mark(student.highest):<10}{student.grade:<6}"
        )


def print_class_stats(students: List[Student]) -> None:
    """Print overall average, top scorer and lowest scorer."""
    print()
    print("Class Stats:")

    if not students:
        print("No valid student records found.")
        return

    overall_average = round(sum(s.average for s in students) / len(students), 2)
    top_scorer = max(students, key=lambda s: s.average)
    lowest_scorer = min(students, key=lambda s: s.average)

    print(f"Overall Average: {overall_average:.2f}")
    print(f"Top Scorer: {top_scorer.name} ({top_scorer.average:.2f})")
    print(f"Lowest Scorer: {lowest_scorer.name} ({lowest_scorer.average:.2f})")


def main(filename: str = "students.txt") -> None:
    students = load_students(filename)
    print_table(students)
    print_class_stats(students)


if __name__ == "__main__":
    main()
