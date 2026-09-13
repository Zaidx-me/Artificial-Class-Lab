from grades import Student, load, parse_line, render
import pytest


def test_letter_grades():
    assert Student("a", 85, 85, 85).letter_grade == "A"
    assert Student("b", 70, 70, 70).letter_grade == "B"
    assert Student("c", 60, 60, 60).letter_grade == "C"
    assert Student("d", 50, 50, 50).letter_grade == "D"
    assert Student("f", 49, 49, 49).letter_grade == "F"


def test_average_speed():
    s = Student("Ali", 78, 85, 90)
    assert s.average == 84.33
    assert s.highest == 90


def test_parse_line_rejects_bad_input():
    assert parse_line("Broken") is None
    assert parse_line("Zahid,invalid,80,90") is None
    ok = parse_line("Ali,78,85,90")
    assert ok is not None and ok.name == "Ali"


def test_render_contains_stats(tmp_path):
    f = tmp_path / "students.txt"
    f.write_text("Ali,78,85,90\nHamza,92,88,95\n")
    out = render(load(str(f)))
    assert "Overall Average" in out
    assert "Top Scorer: Hamza" in out