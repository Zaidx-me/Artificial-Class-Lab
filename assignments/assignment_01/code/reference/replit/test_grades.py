import grades
import pytest


def test_grade_boundaries():
    assert grades.grade(85) == "A"
    assert grades.grade(84.99) == "B"
    assert grades.grade(70) == "B"
    assert grades.grade(60) == "C"
    assert grades.grade(50) == "D"
    assert grades.grade(49.99) == "F"


def test_process_students():
    raw = [{"name": "Ali", "marks": [78, 85, 90]},
           {"name": "Sara", "marks": [62, 70, 55]}]
    result = grades.process(raw)
    assert len(result) == 2
    assert result[0]["average"] == 84.33
    assert result[0]["grade"] == "B"
    assert result[0]["highest"] == 90
    assert result[1]["average"] == 62.33
    assert result[1]["grade"] == "C"


def test_read_students_skips_invalid(tmp_path):
    good = tmp_path / "students.txt"
    good.write_text("Ali,78,85,90\nBad\nHamza,92,88,95\n")
    result = grades.read_students(str(good))
    assert len(result) == 2
    assert result[0]["name"] == "Ali"
    assert result[1]["name"] == "Hamza"
