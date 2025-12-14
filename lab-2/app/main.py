import sys
from app.models import Student
from app import processing as proc
from app import io_utils as io
from app.errors import AppError

def print_menu():
    print("\n--- Menu ---")
    print("1. Upload CSV")
    print("2. Save CSV")
    print("3. Show all students")
    print("4. Add student")
    print("5. Remove student by ID")
    print("6. Update grades by ID")
    print("7. Group stats")
    print("8. Export TOP-N (by average grade)")
    print("9. Sort and show")
    print("0. Exit")

def main():
    students: list[Student] = []
    
    while True:
        print_menu()
        choice = input("Choose option: ").strip()
        
        try:
            if choice == "1":
                path = input("Enter path to CSV file (default: data/students.csv): ").strip()
                if not path: path = "data/students.csv"
                students = io.load_from_csv(path)
                print(f"{len(students)} students were uploaded.")

            elif choice == "2":
                path = input("Enter path for saving CSV file: ").strip()
                io.save_to_csv(path, students)
                print("Saved.")

            elif choice == "3":
                if not students:
                    print("List is empty.")
                else:
                    print(f"{'ID':<5} {'Name':<20} {'Avg':<5} {'Grades'}")
                    for s in students:
                        print(f"{s.id:<5} {s.name:<20} {s.average:<5.2f} {s.grades}")

            elif choice == "4":
                try:
                    s_id = int(input("ID: "))
                    name = input("Name: ")
                    grades_str = input("Grades (separated with spaces): ")
                    grades = [int(g) for g in grades_str.split()] if grades_str else []
                    proc.create_student(students, s_id, name, grades)
                    print("Student was added.")
                except ValueError:
                    print("Error: ID and grades whould be valid integers.")

            elif choice == "5":
                try:
                    s_id = int(input("ID for removing: "))
                    proc.remove_student(students, s_id)
                    print("Student was removed.")
                except ValueError:
                    print("ID sould be valid integer.")

            elif choice == "6":
                try:
                    s_id = int(input("Student ID: "))
                    grades_str = input("New grades (separated with spaces): ")
                    grades = [int(g) for g in grades_str.split()]
                    proc.update_grades(students, s_id, grades)
                    print("Grades were updated.")
                except ValueError:
                    print("Incorrect grades.")

            elif choice == "7":
                stats = proc.get_group_stats(students)
                print(f"Total students: {stats['count']}")
                print(f"Overall average grade: {stats['overall_avg']:.2f}")
                if stats['best']:
                    print(f"Best student: {stats['best'].name} ({stats['best'].average:.2f})")
                if stats['worst']:
                    print(f"Worst student: {stats['worst'].name} ({stats['worst'].average:.2f})")

            elif choice == "8":
                try:
                    n = int(input("Count (N): "))
                    path = input("Export path: ").strip()
                    top_n = proc.get_top_n_students(students, n)
                    io.export_top_n_csv(path, top_n)
                    print(f"TOP-{n} was exported.")
                except ValueError:
                    print("N should be positive integer.")

            elif choice == "9":
                crit = input("Criterion (avg, name, id): ").strip()
                sorted_list = proc.sort_students(students, crit)
                for s in sorted_list:
                    print(f"{s.id} {s.name} (Avg: {s.average:.2f})")

            elif choice == "0":
                print("Exit.")
                break
            
            else:
                print("Incorrect option.")

        except AppError as e:
            print(f"Application error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()