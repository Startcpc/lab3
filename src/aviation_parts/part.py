from dataclasses import dataclass
from math import isfinite
from .errors import InvalidPartError


@dataclass(frozen=True)
class AviationPart:
    """Моделька"""
    id: str
    name: str
    category: str
    year: int
    weight: float
    material: str

    def __post_init__(self) -> None:
        """проверяет данные авиационной детали"""
        for value in (self.id, self.name, self.category, self.material):
            if not isinstance(value, str) or not value.strip():
                raise InvalidPartError("текстовые поля должны быть непустыми")
        if type(self.year) is not int or not(1900 <= self.year <= 2026):
            raise InvalidPartError("некорректный год")
        if type(self.weight) not in (int, float):
            raise InvalidPartError("масса должна быть числом")
        if self.weight <= 0 or not isfinite(self.weight):
            raise InvalidPartError("некорректная масса")
