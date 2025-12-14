import csv
import os
from app.models import Student
from app.errors import FileError

def load_from_csv(filename: str) -> list[Student]:
    if not os.path.exists(filename):
        raise FileError(f"File {filename} was not found.")
    
    students = []
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
            if not rows:
                return []

            start_idx = 0

            # Skip header row if exists
            if rows[0] and not rows[0][0].isdigit():
                start_idx = 1
            
            for row_idx, row in enumerate(rows[start_idx:], start=start_idx+1):
                if not row: continue
                try:
                    s_id = int(row[0])
                    name = row[1]
                    grades = []
                    for val in row[2:]:
                        if val.strip():
                            grades.append(int(val))
                    
                    # Skip duplicated rows
                    if any(s.id == s_id for s in students):
                        print(f"Warning: duplicated ID {s_id} in row {row_idx}. Row was skiped.")
                        continue
                        
                    students.append(Student(s_id, name, grades))
                except (ValueError, IndexError):
                    print(f"Error while parsing row {row_idx}: {row}.")
    except Exception as e:
        raise FileError(f"Error reading CSV: {e}")
    
    return students

def save_to_csv(filename: str, students: list[Student]) -> None:
    try:
        max_grades = 0
        if students:
            max_grades = max(len(s.grades) for s in students)
        
        header = ["id", "name"] + [f"grade{i+1}" for i in range(max_grades)]
        
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for s in students:
                row = [s.id, s.name] + s.grades
                writer.writerow(row)
    except Exception as e:
        raise FileError(f"Error writing CSV: {e}")

def export_top_n_csv(filename: str, students: list[Student]) -> None:
    try:
        header = ["id", "name", "average", "grades"]
        with open(filename, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for s in students:
                grades_str = " ".join(map(str, s.grades))
                writer.writerow([s.id, s.name, f"{s.average:.2f}", grades_str])
    except Exception as e:
        raise FileError(f"Error while exporting: {e}")