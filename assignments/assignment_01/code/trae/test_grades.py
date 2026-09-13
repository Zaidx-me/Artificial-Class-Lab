import pytest
from grades import compute_grade, compute_student_metrics, parse_line, compute_class_stats


def test_compute_grade():
    assert compute_grade(90) == 'A'
    assert compute_grade(85) == 'A'
    assert compute_grade(84.99) == 'B'
    assert compute_grade(70) == 'B'
    assert compute_grade(69.99) == 'C'
    assert compute_grade(60) == 'C'
    assert compute_grade(59.99) == 'D'
    assert compute_grade(50) == 'D'
    assert compute_grade(49.99) == 'F'
    assert compute_grade(0) == 'F'


def test_compute_student_metrics():
    student = {'name': 'Ali', 'mark1': 78, 'mark2': 85, 'mark3': 90}
    result = compute_student_metrics(student)
    assert result['name'] == 'Ali'
    assert result['average'] == 84.33
    assert result['highest'] == 90
    assert result['grade'] == 'B'

    student2 = {'name': 'Hamza', 'mark1': 92, 'mark2': 88, 'mark3': 95}
    result2 = compute_student_metrics(student2)
    assert result2['average'] == 91.67
    assert result2['highest'] == 95
    assert result2['grade'] == 'A'


def test_parse_line_and_invalid_lines(capsys):
    valid = parse_line('Ali,78,85,90')
    assert valid is not None
    assert valid['name'] == 'Ali'
    assert valid['mark1'] == 78
    assert valid['mark2'] == 85
    assert valid['mark3'] == 90

    invalid_missing = parse_line('Sara,62,70')
    captured = capsys.readouterr()
    assert invalid_missing is None
    assert 'Warning: skipping invalid line' in captured.err

    invalid_marks = parse_line('Bad,abc,def,ghi')
    captured = capsys.readouterr()
    assert invalid_marks is None
    assert 'Warning: skipping invalid line' in captured.err

    empty_line = parse_line('')
    assert empty_line is None

    whitespace_only = parse_line('   ')
    assert whitespace_only is None
