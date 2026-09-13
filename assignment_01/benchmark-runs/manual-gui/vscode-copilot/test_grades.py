from grades import calculate_student, read_students


def test_calculate_student_rounds_average_and_assigns_grade():
    student = calculate_student("Ali", [78, 85, 90])

    assert student == {
        "name": "Ali",
        "average": 84.33,
        "highest": 90,
        "grade": "B",
    }


def test_read_students_skips_invalid_lines(tmp_path):
    input_file = tmp_path / "students.txt"
    input_file.write_text("Valid,80,80,80\nBroken,not-a-mark,70,80\nTooFew,90,90\n")

    students, warnings = read_students(input_file)

    assert [student["name"] for student in students] == ["Valid"]
    assert len(warnings) == 2
    assert "line 2" in warnings[0]
    assert "line 3" in warnings[1]


def test_sample_data_has_expected_class_statistics():
    students, warnings = read_students("students.txt")

    assert warnings == []
    assert round(sum(float(student["average"]) for student in students) / len(students), 2) == 71.33
    assert max(students, key=lambda student: float(student["average"]))["name"] == "Hamza"
    assert min(students, key=lambda student: float(student["average"]))["name"] == "Ayesha"
