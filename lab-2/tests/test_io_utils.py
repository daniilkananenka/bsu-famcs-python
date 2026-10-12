import pytest
from lab import io_utils
from lab.models import Student
from lab.errors import FileError

def test_save_and_load_roundtrip(tmp_path):
    file_path = tmp_path / "test_students.csv"
    original_students = [
        Student(1, "Alice", [10, 20]),
        Student(2, "Bob", [100]),
        Student(3, "Charlie", [])
    ]

    io_utils.save_to_csv(str(file_path), original_students)

    loaded_students = io_utils.load_from_csv(str(file_path))

    assert len(loaded_students) == 3
    assert loaded_students[0].name == "Alice"
    assert loaded_students[0].grades == [10, 20]
    assert loaded_students[2].grades == []

def test_load_non_existent_file():
    with pytest.raises(FileError):
        io_utils.load_from_csv("non_existent_file_12345.csv")

def test_load_corrupted_data(tmp_path):
    file_path = tmp_path / "bad_data.csv"
    content = """id,name,grade1
    1,Valid User,50
    abc,Invalid ID,50
    2,Bad Grade,xyz
    3,Normal User,
    """
    file_path.write_text(content, encoding="utf-8")

    students = io_utils.load_from_csv(str(file_path))
    
    ids = [s.id for s in students]
    assert 1 in ids
    assert 3 in ids
    assert "abc" not in ids

def test_export_top_n(tmp_path):
    file_path = tmp_path / "top.csv"
    students = [
        Student(1, "Looser", [10]),
        Student(2, "Winner", [100])
    ]
    
    io_utils.export_top_n_csv(str(file_path), students)
    
    content = file_path.read_text(encoding="utf-8")
    assert "Winner" in content
    assert "100.00" in content