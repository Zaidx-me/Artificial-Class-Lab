"""Student Grades Manager — a small CLI that converts a CSV of marks into a report.

Reads ``students.txt`` (Name,Mark1,Mark2,Mark3 per line), skips malformed lines with
a warning on stderr, and prints a formatted table plus class statistics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import logging
import sys

logger = logging.getLogger("grades")


@dataclass(frozen=True)
class Student:
    name: str
    mark1: float
    mark2: float
    mark3: float

    @property
    def average(self) -> float:
        return round((self.mark1 + self.mark2 + self.mark3) / 3, 2)

    @property
    def highest(self) -> float:
        return max(self.mark1, self.mark2, self.mark3)

    @property
    def letter_grade(self) -> str:
        if self.average >= 85:
            return "A"
        if self.average >= 70:
            return "B"
        if self.average >= 60:
            return "C"
        if self.average >= 50:
            return "D"
        return "F"


def parse_line(line: str) -> Student | None:
    parts = [part.strip() for part in line.split(",")]
    if len(parts) != 4 or not parts[0]:
        logger.warning("Skipping malformed line: %s", line)
        return None
    try:
        mark1, mark2, mark3 = (float(parts[1]), float(parts[2]), float(parts[3]))
    except ValueError:
        logger.warning("Skipping non-numeric line: %s", line)
        return None
    return Student(parts[0], mark1, mark2, mark3)


def load(filename: str = "students.txt") -> list[Student]:
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"Data file not found: {filename}")
    students: list[Student] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if student := parse_line(line):
            students.append(student)
    return students


def render(students: list[Student]) -> str:
    rows = [f"{'Name':<12}{'Average':<9}{'Highest':<9}Grade",
            "-" * 39]
    for s in students:
        rows.append(f"{s.name:<12}{s.average:<9.2f}{s.highest:<9.1f}{s.letter_grade}")
    stats = compute_stats(students)
    if stats:
        rows += [
            "",
            "Class Stats:",
            f"Overall Average: {stats['overall']:.2f}",
            f"Top Scorer: {stats['top'].name} ({stats['top'].average:.2f})",
            f"Lowest Scorer: {stats['bottom'].name} ({stats['bottom'].average:.2f})",
        ]
    return "\n".join(rows)


def compute_stats(students: list[Student]) -> dict | None:
    if not students:
        return None
    overall = round(sum(s.average for s in students) / len(students), 2)
    return {
        "overall": overall,
        "top": max(students, key=lambda s: s.average),
        "bottom": min(students, key=lambda s: s.average),
    }


def main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        students = load()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    print(render(students))


if __name__ == "__main__":
    main()