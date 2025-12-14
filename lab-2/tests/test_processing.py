import pytest
from app import processing as proc
from app.errors import ValidationError, StudentNotFoundError

def test_create_student_valid():
    students = []
    s = proc.create_student(students, 1, "New", [50])
    assert len(students) == 1
    assert s.name == "New"

def test_create_student_duplicate_id(sample_students):
    with pytest.raises(ValidationError):
        proc.create_student(sample_students, 1, "Dup", [])

def test_validate_grades():
    with pytest.raises(ValidationError):
        proc.validate_student_data(1, "Test", [101])

def test_remove_student(sample_students):
    proc.remove_student(sample_students, 1)
    assert len(sample_students) == 2
    assert sample_students[0].id == 2

def test_remove_missing_student(sample_students):
    with pytest.raises(StudentNotFoundError):
        proc.remove_student(sample_students, 999)

def test_sort_students_avg(sample_students):
    # Anna(100) -> Ivan(85) -> Petr(65)
    sorted_s = proc.sort_students(sample_students, "avg")
    assert sorted_s[0].name == "Anna"
    assert sorted_s[-1].name == "Petr"