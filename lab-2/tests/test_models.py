from app.models import Student

def test_student_average():
    s = Student(1, "Test", [10, 20, 30])
    assert s.average == 20.0

def test_student_average_empty():
    s = Student(1, "Test", [])
    assert s.average == 0.0