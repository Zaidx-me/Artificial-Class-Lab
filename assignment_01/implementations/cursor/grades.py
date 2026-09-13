from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass
class Student:
    name: str
    mark1: float
    mark2: float
    mark3: float

    @property
    def marks(self) -> list[float]:
        return [self.mark1, self.mark2, self.mark3]

    @property
    def average(self) -> float:
        return round(sum(self.marks) / len(self.marks), 2)

    @property
    def highest(self) -> float:
        return max(self.marks)

    @property
    def grade(self) -> str:
        thresholds = [(85, "A"), (70, "B"), (60, "C"), (50, "D")]
        for bound, letter in thresholds:
            if self.average >= bound:
                return letter
        return "F"


def load_students(path: str = "students.txt") -> list[Student]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing data file: {path}")

    students: list[Student] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [piece.strip() for piece in line.split(",")]
        if len(parts) != 4 or not parts[0]:
            print(f"WARNING: skipping malformed line: {line!r}", file=sys.stderr)
            continue
        try:
            marks = [float(x) for x in parts[1:4]]
        except ValueError:
            print(f"WARNING: skipping non-numeric line: {line!r}", file=sys.stderr)
            continue
        students.append(Student(parts[0], *marks))
    return students


def render_report(students: list[Student]) -> str:
    header = f"{'Name':<12}{'Average':<10}{'Highest':<10} Grade"
    rows = [header, "-" * 40]
    for s in students:
        rows.append(
            f"{s.name:<12}{s.average:<10.2f}{s.highest:<10.1f} {s.grade}"
        )

    if students:
        overall = round(sum(s.average for s in students) / len(students), 2)
        top = max(students, key=lambda s: s.average)
        bottom = min(students, key=lambda s: s.average)
        rows.extend(
            [
                "",
                "Class Stats:",
                f"Overall Average: {overall:.2f}",
                f"Top Scorer: {top.name} ({top.average:.2f})",
                f"Lowest Scorer: {bottom.name} ({bottom.average:.2f})",
            ]
        )
    return "\n".join(rows)


def main() -> None:
    try:
        students = load_students()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    print(render_report(students))


if __name__ == "__main__":
    main()