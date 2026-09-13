from grades import Student, load_students, render_report
import pytest


def test_grade_boundaries():
    assert Student("x", 85, 85, 85).grade == "A"
    assert Student("x", 70, 70, 70).grade == "B"
    assert Student("x", 60, 60, 60).grade == "C"
    assert Student("x", 50, 50, 50).grade == "D"
    assert Student("x", 40, 40, 40).grade == "F"


def test_average_rounding_and_highest():
    s = Student("Ali", 78, 85, 90)
    assert s.average == 84.33
    assert s.highest == 90


def test_load_skips_malformed(tmp_path):
    f = tmp_path / "students.txt"
    f.write_text("Ali,78,85,90\nBad\nHamza,92,88,95\n")
    students = load_students(str(f))
    assert [s.name for s in students] == ["Ali", "Hamza"]