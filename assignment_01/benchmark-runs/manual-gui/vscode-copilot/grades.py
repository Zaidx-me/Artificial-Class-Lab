"""Student grades manager CLI."""

from pathlib import Path


GRADE_THRESHOLDS = ((85, "A"), (70, "B"), (60, "C"), (50, "D"))


def letter_grade(average: float) -> str:
    """Return the letter grade for an average mark."""
    for threshold, grade in GRADE_THRESHOLDS:
        if average >= threshold:
            return grade
    return "F"


def calculate_student(name: str, marks: list[float]) -> dict[str, object]:
    """Calculate summary values for one student."""
    average = round(sum(marks) / len(marks), 2)
    return {
        "name": name,
        "average": average,
        "highest": max(marks),
        "grade": letter_grade(average),
    }


def read_students(path: str | Path) -> tuple[list[dict[str, object]], list[str]]:
    """Read valid student records and return warnings for invalid lines."""
    students = []
    warnings = []

    with open(path, encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                continue
            parts = [part.strip() for part in line.split(",")]
            try:
                if len(parts) != 4 or not parts[0]:
                    raise ValueError("expected name and three marks")
                marks = [float(mark) for mark in parts[1:]]
                if any(mark < 0 or mark > 100 for mark in marks):
                    raise ValueError("marks must be between 0 and 100")
            except ValueError:
                warnings.append(f"Warning: skipped invalid line {line_number}: {line}")
                continue
            students.append(calculate_student(parts[0], marks))

    return students, warnings


def print_report(students: list[dict[str, object]], warnings: list[str]) -> None:
    """Print the student table and class statistics."""
    print("Name        Average   Highest   Grade")
    print("--------------------------------------")
    for student in students:
        print(
            f"{student['name']:<12}{student['average']:>7.2f}"
            f"{student['highest']:>10.0f}   {student['grade']}"
        )

    for warning in warnings:
        print(warning)

    if not students:
        return

    overall_average = round(
        sum(float(student["average"]) for student in students) / len(students), 2
    )
    top_scorer = max(students, key=lambda student: float(student["average"]))
    lowest_scorer = min(students, key=lambda student: float(student["average"]))

    print("\nClass Stats:")
    print(f"Overall Average: {overall_average:.2f}")
    print(f"Top Scorer: {top_scorer['name']} ({float(top_scorer['average']):.2f})")
    print(f"Lowest Scorer: {lowest_scorer['name']} ({float(lowest_scorer['average']):.2f})")


def main() -> None:
    """Run the grades report for students.txt."""
    students, warnings = read_students(Path(__file__).with_name("students.txt"))
    print_report(students, warnings)


if __name__ == "__main__":
    main()
