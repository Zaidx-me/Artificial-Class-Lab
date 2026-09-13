from grades import letter_for, report, rows_from
import pytest


def test_letter_for():
    assert letter_for(85) == "A"
    assert letter_for(84) == "B"
    assert letter_for(70) == "B"
    assert letter_for(69) == "C"
    assert letter_for(50) == "D"
    assert letter_for(49) == "F"


def test_rows_and_report():
    data = list(rows_from("students.txt"))
    assert len(data) == 5
    assert data[0].average == 84.33
    assert data[0].grade == "B"
    out = report("students.txt")
    assert "Cohort Statistics" in out
    assert "Mean grade:" in out


def test_skips_invalid(tmp_path):
    f = tmp_path / "students.txt"
    f.write_text("Ali,78,85,90\nBrokenLine\nZahid,invalid,80,90\nHamza,92,88,95\n")
    data = list(rows_from(str(f)))
    assert [d.name for d in data] == ["Ali", "Hamza"]