"""grades.py — Student Grades Manager (Aider-style, concise)."""

import sys

MARKS = ["mark1", "mark2", "mark3"]


def read_rows(path="students.txt"):
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if "," not in line:
                print(f"warn: skipped '{line}'", file=sys.stderr)
                continue
            name, *marks = [x.strip() for x in line.split(",")]
            if len(marks) != 3 or not name:
                print(f"warn: skipped '{line}'", file=sys.stderr)
                continue
            try:
                marks = [float(m) for m in marks]
            except ValueError:
                print(f"warn: skipped '{line}'", file=sys.stderr)
                continue
            rows.append({"name": name, "marks": marks})
    return rows


def grade(avg):
    return next((g for t, g in [(85, "A"), (70, "B"), (60, "C"), (50, "D")]
                 if avg >= t), "F")


def build(rows):
    out = []
    for r in rows:
        avg = round(sum(r["marks"]) / 3, 2)
        out.append({"name": r["name"], "avg": avg,
                    "max": max(r["marks"]), "grade": grade(avg)})
    return out


def show(data):
    lines = [f"{'Name':<12}{'Average':<10}{'Highest':<10}Grade", "-" * 42]
    for d in data:
        lines.append(f"{d['name']:<12}{d['avg']:<10.2f}{d['max']:<10.0f}{d['grade']}")
    if data:
        overall = round(sum(d["avg"] for d in data) / len(data), 2)
        top = max(data, key=lambda d: d["avg"])
        low = min(data, key=lambda d: d["avg"])
        lines += [f"\nClass Stats:\nOverall Average: {overall:.2f}",
                  f"Top Scorer: {top['name']} ({top['avg']:.2f})",
                  f"Lowest Scorer: {low['name']} ({low['avg']:.2f})"]
    print("\n".join(lines))


def main():
    try:
        data = read_rows()
    except FileNotFoundError:
        sys.exit("students.txt not found")
    show(build(data))


if __name__ == "__main__":
    main()