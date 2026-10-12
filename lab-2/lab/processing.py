from typing import Optional
from lab.models import Student
from lab.errors import ValidationError, StudentNotFoundError

def validate_student_data(student_id: int, name: str, grades: list[int]) -> None:
    if student_id < 0:
        raise ValidationError("ID should be positive integer")
    if not name.strip():
        raise ValidationError("Name should not be empty")
    for g in grades:
        if not (0 <= g <= 100):
            raise ValidationError(f"Grade {g} is out of range (0-100)")

def create_student(students: list[Student], s_id: int, name: str, grades: list[int]) -> Student:
    if any(s.id == s_id for s in students):
        raise ValidationError(f"Student with ID {s_id} is already existed")
    validate_student_data(s_id, name, grades)
    new_student = Student(id=s_id, name=name, grades=grades)
    students.append(new_student)
    return new_student

def remove_student(students: list[Student], s_id: int) -> None:
    for i, s in enumerate(students):
        if s.id == s_id:
            del students[i]
            return
    raise StudentNotFoundError(f"Student with ID {s_id} was not found")

def update_grades(students: list[Student], s_id: int, new_grades: list[int]) -> None:
    for s in students:
        if s.id == s_id:
            for g in new_grades:
                if not (0 <= g <= 100):
                    raise ValidationError(f"Grade {g} is out of range (0-100)")
            s.grades = new_grades
            return
    raise StudentNotFoundError(f"Student with ID {s_id} was not found")

def get_group_stats(students: list[Student]) -> dict:
    if not students:
        return {"count": 0, "overall_avg": 0.0, "best": None, "worst": None}
    
    all_grades = [g for s in students for g in s.grades]
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0.0
    
    sorted_by_avg = sorted(students, key=lambda s: s.average)
    
    return {
        "count": len(students),
        "overall_avg": overall_avg,
        "best": sorted_by_avg[-1],
        "worst": sorted_by_avg[0]
    }

def sort_students(students: list[Student], criterion: str) -> list[Student]:
    if criterion == "avg":
        return sorted(students, key=lambda s: (-s.average, s.name))
    elif criterion == "name":
        return sorted(students, key=lambda s: s.name)
    elif criterion == "id":
        return sorted(students, key=lambda s: s.id)
    return students

def get_top_n_students(students: list[Student], n: int) -> list[Student]:
    sorted_s = sort_students(students, "avg")
    return sorted_s[:n]