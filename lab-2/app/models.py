from dataclasses import dataclass, field

@dataclass
class Student:
    id: int
    name: str
    grades: list[int] = field(default_factory=list)

    @property
    def average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)