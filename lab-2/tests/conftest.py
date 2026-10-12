import pytest
from lab.models import Student

@pytest.fixture
def sample_students():
    return [
        Student(1, "Ivan", [80, 90]),
        Student(2, "Petr", [60, 70]),
        Student(3, "Anna", [100, 100])
    ]