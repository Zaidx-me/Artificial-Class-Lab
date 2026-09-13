import sys
import os


def parse_line(line):
    line = line.strip()
    if not line:
        return None
    parts = line.split(',')
    if len(parts) != 4:
        print(f"Warning: skipping invalid line: {line}", file=sys.stderr)
        return None
    name = parts[0].strip()
    if not name:
        print(f"Warning: skipping invalid line: {line}", file=sys.stderr)
        return None
    try:
        m1 = float(parts[1].strip())
        m2 = float(parts[2].strip())
        m3 = float(parts[3].strip())
    except ValueError:
        print(f"Warning: skipping invalid line: {line}", file=sys.stderr)
        return None
    return {'name': name, 'mark1': m1, 'mark2': m2, 'mark3': m3}


def compute_grade(average):
    if average >= 85:
        return 'A'
    elif average >= 70:
        return 'B'
    elif average >= 60:
        return 'C'
    elif average >= 50:
        return 'D'
    else:
        return 'F'


def compute_student_metrics(student):
    marks = [student['mark1'], student['mark2'], student['mark3']]
    average = round(sum(marks) / 3, 2)
    highest = max(marks)
    grade = compute_grade(average)
    return {
        'name': student['name'],
        'average': average,
        'highest': highest,
        'grade': grade
    }


def read_students(filename='students.txt'):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    students = []
    with open(filename, 'r') as f:
        for line in f:
            parsed = parse_line(line)
            if parsed is not None:
                students.append(parsed)
    return students


def process_all_students(raw_students):
    return [compute_student_metrics(s) for s in raw_students]


def format_table(students):
    lines = []
    header = f"{'Name':<12}{'Average':<10}{'Highest':<10}{'Grade'}"
    lines.append(header)
    lines.append('-' * 38)
    for s in students:
        avg_str = f"{s['average']:.2f}"
        highest_str = f"{int(s['highest'])}" if s['highest'] == int(s['highest']) else f"{s['highest']}"
        line = f"{s['name']:<12}{avg_str:<10}{highest_str:<10}{s['grade']}"
        lines.append(line)
    return '\n'.join(lines)


def compute_class_stats(students):
    if not students:
        return None
    overall_avg = round(sum(s['average'] for s in students) / len(students), 2)
    top = max(students, key=lambda s: s['average'])
    lowest = min(students, key=lambda s: s['average'])
    return {
        'overall_average': overall_avg,
        'top_scorer': top,
        'lowest_scorer': lowest
    }


def format_stats(stats):
    if stats is None:
        return ''
    lines = []
    lines.append('')
    lines.append('Class Stats:')
    lines.append(f"Overall Average: {stats['overall_average']:.2f}")
    lines.append(f"Top Scorer: {stats['top_scorer']['name']} ({stats['top_scorer']['average']:.2f})")
    lines.append(f"Lowest Scorer: {stats['lowest_scorer']['name']} ({stats['lowest_scorer']['average']:.2f})")
    return '\n'.join(lines)


def main():
    raw_students = read_students()
    students = process_all_students(raw_students)
    print(format_table(students))
    stats = compute_class_stats(students)
    print(format_stats(stats))


if __name__ == '__main__':
    main()
