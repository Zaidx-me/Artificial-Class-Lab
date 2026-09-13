from grades import Student, parse_records


def test_student_statistics_and_grade():
    student = Student("Ali", (78, 85, 90))
    assert student.average == 84.33333333333333
    assert student.highest == 90
    assert student.grade == "B"


def test_parse_records_skips_invalid_lines_with_warning():
    students, warnings = parse_records(["Valid,80,70,90\n", "bad line\n", "TooHigh,101,50,50\n"])
    assert [student.name for student in students] == ["Valid"]
    assert len(warnings) == 2
    assert "line 2" in warnings[0]


def test_class_average_and_extremes():
    students, warnings = parse_records(
        ["Ali,78,85,90", "Sara,62,70,55", "Hamza,92,88,95"]
    )
    assert not warnings
    assert round(sum(student.average for student in students) / len(students), 2) == 79.44
    assert max(students, key=lambda student: student.average).name == "Hamza"
    assert min(students, key=lambda student: student.average).name == "Sara"
