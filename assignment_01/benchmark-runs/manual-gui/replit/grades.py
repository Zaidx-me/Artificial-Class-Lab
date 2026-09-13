import sys
from pathlib import Path


def read_students(filename: str = "students.txt") -> list[dict]:
    results: list[dict] = []
    path = Path(filename)
    if not path.exists():
        print(f"Error: file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 4 or not parts[0]:
            print(f"Warning: skipping invalid line: {line}", file=sys.stderr)
            continue
        try:
            m1, m2, m3 = float(parts[1]), float(parts[2]), float(parts[3])
        except ValueError:
            print(f"Warning: skipping invalid line: {line}", file=sys.stderr)
            continue
        results.append({"name": parts[0], "marks": [m1, m2, m3]})
    return results


def grade(avg: float) -> str:
    for threshold, letter in [(85, "A"), (70, "B"), (60, "C"), (50, "D")]:
        if avg >= threshold:
            return letter
    return "F"


def process(students: list[dict]) -> list[dict]:
    return [
        {
            "name": s["name"],
            "average": round(sum(s["marks"]) / 3, 2),
            "highest": max(s["marks"]),
            "grade": grade(round(sum(s["marks"]) / 3, 2)),
        }
        for s in students
    ]


def fmt(results: list[dict]) -> str:
    if not results:
        return ""
    header = f"{'Name':<12}{'Average':<10}{'Highest':<10}Grade"
    sep = "-" * 40
    rows = [
        f"{r['name']:<12}{r['average']:<10.2f}{int(r['highest']):<10}{r['grade']}"
        for r in results
    ]
    avg = round(sum(r["average"] for r in results) / len(results), 2)
    top = max(results, key=lambda r: r["average"])
    bot = min(results, key=lambda r: r["average"])
    stats = [
        "",
        "Class Stats:",
        f"Overall Average: {avg:.2f}",
        f"Top Scorer: {top['name']} ({top['average']:.2f})",
        f"Lowest Scorer: {bot['name']} ({bot['average']:.2f})",
    ]
    return "\n".join([header, sep, *rows, *stats])


if __name__ == "__main__":
    print(fmt(process(read_students())))
