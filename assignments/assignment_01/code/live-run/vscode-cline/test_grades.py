"""Unit tests for grades.py, run with pytest."""

from grades import Student, letter_grade, parse_line, load_students


def test_student_average_highest_and_grade():
    student = Student(name="Ali", marks=[78, 85, 90])
    assert student.average == 84.33
    assert student.highest == 90
    assert student.grade == "B"

    assert letter_grade(90) == "A"
    assert letter_grade(85) == "A"
    assert letter_grade(70) == "B"
    assert letter_grade(60) == "C"
    assert letter_grade(50) == "D"
    assert letter_grade(49.99) == "F"


def test_parse_line_valid_and_invalid():
    valid = parse_line("Hamza,92,88,95")
    assert valid is not None
    assert valid.name == "Hamza"
    assert valid.marks == [92.0, 88.0, 95.0]

    # Wrong number of fields
    assert parse_line("Invalid,Line") is None
    # Non-numeric marks
    assert parse_line("Bad,abc,88,95") is None
    # Empty line
    assert parse_line("") is None


def test_load_students_skips_invalid_lines(tmp_path):
    content = (
        "Ali,78,85,90\n"
        "InvalidLine\n"
        "Sara,62,70,55\n"
        "Bad,x,y,z\n"
    )
    file_path = tmp_path / "students.txt"
    file_path.write_text(content)

    students = load_students(str(file_path))

    assert len(students) == 2
    assert students[0].name == "Ali"
    assert students[1].name == "Sara"
