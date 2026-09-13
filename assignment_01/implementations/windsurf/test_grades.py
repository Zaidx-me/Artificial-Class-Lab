from grades import classify, parse_record, read_file, summarize
import pytest


def test_classify():
    assert classify(85) == "A"
    assert classify(70) == "B"
    assert classify(60) == "C"
    assert classify(50) == "D"
    assert classify(49) == "F"


def test_parse_and_summarize():
    data = [parse_record("Ali,78,85,90")]
    assert data[0]["name"] == "Ali"
    rows = summarize(data)
    assert rows[0]["avg"] == 84.33
    assert rows[0]["max"] == 90
    assert rows[0]["grade"] == "B"


def test_read_file_skips_bad_lines(tmp_path):
    f = tmp_path / "d.txt"
    f.write_text("Ali,78,85,90\nbroken\nHamza,92,88,95\n")
    names = [r["name"] for r in read_file(str(f))]
    assert names == ["Ali", "Hamza"]