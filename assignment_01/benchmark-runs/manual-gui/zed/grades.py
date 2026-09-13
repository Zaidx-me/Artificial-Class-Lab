"""Student grades manager CLI."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, TextIO


@dataclass(frozen=True)
class Student:
    """A student's marks and derived statistics."""

    name: str
    marks: tuple[float, float, float]

    @property
    def average(self) -> float:
        return sum(self.marks) / len(self.marks)

    @property
    def highest(self) -> float:
        return max(self.marks)

    @property
    def grade(self) -> str:
        if self.average >= 85:
            return "A"
        if self.average >= 70:
            return "B"
        if self.average >= 60:
            return "C"
        if self.average >= 50:
            return "D"
        return "F"


def parse_records(lines: Iterable[str]) -> tuple[list[Student], list[str]]:
    """Parse records, returning valid students and warning messages."""
    students: list[Student] = []
    warnings: list[str] = []

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line:
            continue
        fields = [field.strip() for field in line.split(",")]
        if len(fields) != 4 or not fields[0]:
            warnings.append(f"Warning: skipped invalid line {line_number}: {line}")
            continue
        try:
            marks = tuple(float(value) for value in fields[1:])
        except ValueError:
            warnings.append(f"Warning: skipped invalid line {line_number}: {line}")
            continue
        if any(mark < 0 or mark > 100 for mark in marks):
            warnings.append(f"Warning: skipped invalid line {line_number}: {line}")
            continue
        students.append(Student(fields[0], marks))

    return students, warnings


def load_students(path: Path) -> tuple[list[Student], list[str]]:
    """Load and parse students from *path*."""
    with path.open(encoding="utf-8") as file:
        return parse_records(file)


def format_mark(mark: float) -> str:
    return f"{mark:.2f}" if mark % 1 else f"{mark:.0f}"


def print_report(students: list[Student], warnings: list[str], output: TextIO = sys.stdout) -> None:
    for warning in warnings:
        print(warning, file=output)

    print("Name        Average   Highest   Grade", file=output)
    print("--------------------------------------", file=output)
    for student in students:
        print(
            f"{student.name:<11}{student.average:>7.2f}   "
            f"{format_mark(student.highest):>7}   {student.grade}",
            file=output,
        )

    if not students:
        print("\nClass Stats:", file=output)
        print("No valid student records.", file=output)
        return

    overall_average = sum(student.average for student in students) / len(students)
    top = max(students, key=lambda student: student.average)
    lowest = min(students, key=lambda student: student.average)
    print("\nClass Stats:", file=output)
    print(f"Overall Average: {overall_average:.2f}", file=output)
    print(f"Top Scorer: {top.name} ({top.average:.2f})", file=output)
    print(f"Lowest Scorer: {lowest.name} ({lowest.average:.2f})", file=output)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("students.txt")
    try:
        students, warnings = load_students(path)
    except FileNotFoundError:
        print(f"Error: could not find {path}", file=sys.stderr)
        return 1
    print_report(students, warnings)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
