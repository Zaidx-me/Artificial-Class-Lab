import argparse
import sys
from pathlib import Path


def parse_record(line: str) -> dict | None:
    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 4 or not parts[0]:
        print(f"Warning: skipping invalid line -> {line}", file=sys.stderr)
        return None
    try:
        marks = [float(parts[1]), float(parts[2]), float(parts[3])]
    except ValueError:
        print(f"Warning: skipping non-numeric line -> {line}", file=sys.stderr)
        return None
    return {"name": parts[0], "marks": marks}


def read_file(path: str) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        print(f"Error: '{path}' not found", file=sys.stderr)
        sys.exit(1)
    return [r for r in (parse_record(l) for l in p.read_text().splitlines()) if r]


def classify(avg: float) -> str:
    if avg >= 85:
        return "A"
    if avg >= 70:
        return "B"
    if avg >= 60:
        return "C"
    if avg >= 50:
        return "D"
    return "F"


def summarize(data: list[dict]) -> list[dict]:
    out = []
    for row in data:
        avg = round(sum(row["marks"]) / 3, 2)
        out.append({"name": row["name"], "avg": avg,
                    "max": max(row["marks"]), "grade": classify(avg)})
    return out


def pretty(rows: list[dict]) -> str:
    header = f"{'Name':<12}{'Average':<10}{'Highest':<10} Grade"
    lines = [header, "=" * 40]
    for r in rows:
        lines.append(f"{r['name']:<12}{r['avg']:<10.2f}{r['max']:<10.1f} {r['grade']}")
    if rows:
        overall = round(sum(r["avg"] for r in rows) / len(rows), 2)
        best = max(rows, key=lambda r: r["avg"])
        worst = min(rows, key=lambda r: r["avg"])
        lines += [
            "",
            "Class Stats:",
            f"Overall Average: {overall:.2f}",
            f"Top Scorer: {best['name']} ({best['avg']:.2f})",
            f"Lowest Scorer: {worst['name']} ({worst['avg']:.2f})",
        ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Student Grades Manager")
    parser.add_argument("-f", "--file", default="students.txt",
                        help="path to data file (default: students.txt)")
    args = parser.parse_args()
    print(pretty(summarize(read_file(args.file))))


if __name__ == "__main__":
    main()