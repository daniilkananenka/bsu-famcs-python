import pytest
from lab.main import main
from lab import processing

def test_cli_add_student_scenario(monkeypatch, capsys):
    inputs = iter(['4', '10', 'John Doe', '50 60', '0'])
    
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    
    assert "Student was added." in captured.out
    assert "Exit." in captured.out

def test_cli_invalid_input_scenario(monkeypatch, capsys):
    inputs = iter(['5', 'not_a_number', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()

    captured = capsys.readouterr()
    assert "ID sould be valid integer." in captured.out

def test_cli_show_empty_list(monkeypatch, capsys):
    inputs = iter(['3', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main()
    captured = capsys.readouterr()
    assert "List is empty." in captured.out