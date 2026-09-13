from grades import build, grade, read_rows
import pytest


def test_grades():
    assert grade(85) == "A"
    assert grade(70) == "B"
    assert grade(60) == "C"
    assert grade(50) == "D"
    assert grade(0) == "F"


def test_build():
    rows = read_rows()
    out = build(rows)
    assert out[0]["avg"] == 84.33
    assert out[0]["grade"] == "B"
    assert out[0]["max"] == 90
    assert len(out) == 5  # malformed lines skipped


def test_read_rows_filter(capsys):
    # uses the repo students.txt which contains 2 invalid lines
    rows = read_rows()
    assert len(rows) == 5
    err = capsys.readouterr().err
    assert "warn" in err