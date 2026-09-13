"""Student Roster Analytics — computes grades, ranking and cohort stats."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator
import locale
import sys


GRADE_CURVE: tuple[tuple[float, str], ...] = (
    (85.0, "A"), (70.0, "B"), (60.0, "C"), (50.0, "D"),
)


@dataclass(slots=True)
class Record:
    name: str
    average: float
    highest: float
    grade: str


def letter_for(score: float) -> str:
    for floor, letter in GRADE_CURVE:
        if score >= floor:
            return letter
    return "F"


def rows_from(path: str) -> Iterator[Record]:
    with open(path, encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            field = [part.strip() for part in line.split(",")]
            if len(field) != 4 or not field[0]:
                print(f"[line {lineno}] skipped invalid record: {line.rstrip()}", file=sys.stderr)
                continue
            try:
                a, b, c = (float(field[1]), float(field[2]), float(field[3]))
            except ValueError:
                print(f"[line {lineno}] skipped non-numeric record: {line.rstrip()}", file=sys.stderr)
                continue
            average = round((a + b + c) / 3, 2)
            yield Record(field[0], average, max(a, b, c), letter_for(average))


def report(path: str) -> str:
    data = list(rows_from(path))
    if not data:
        return "No valid records found."
    grid = [f"{'Name':<12}{'Average':<10}{'Highest':<10}Grade", "-" * 42]
    grid += [f"{r.name:<12}{r.average:<10.2f}{r.highest:<10.1f}{r.grade}" for r in data]
    overall = round(sum(r.average for r in data) / len(data), 2)
    top = max(data, key=lambda r: r.average)
    low = min(data, key=lambda r: r.average)
    grid += [
        "",
        "Cohort Statistics",
        f"Mean grade:       {overall:5.2f}",
        f"Top performer:    {top.name} ({top.average:.2f})",
        f"Lowest performer: {low.name} ({low.average:.2f})",
    ]
    return "\n".join(grid)


def main() -> None:
    locale.setlocale(locale.LC_ALL, "")
    try:
        print(report("students.txt"))
    except FileNotFoundError:
        print("students.txt: no such file", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()