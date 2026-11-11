from json import dump
import pytest

from src.aviation_parts.part import AviationPart
from src.aviation_parts.catalog import AviationCatalog
from src.aviation_parts.errors import (
    InvalidPartError,
    DuplicateIdError,
    PartNotFoundError,
    CorruptedFileError,
    UnsupportedVersionError,
)


def make_part(part_id: str = "1") -> AviationPart:
    """создает авиационную деталь"""
    return AviationPart(part_id, "крыло", "корпус", 2020, 150.5, "алюминий")


def test_part() -> None:
    """создание допустимой и недопустимой сущности"""
    part = make_part()
    assert part.id == "1"

    with pytest.raises(InvalidPartError):
        make_part("")


def test_add_get_remove() -> None:
    """добавление, получение и удаление"""
    catalog = AviationCatalog()
    part = make_part()

    catalog.add(part)
    assert catalog.get("1") == part

    catalog.remove("1")
    with pytest.raises(PartNotFoundError):
        catalog.get("1")


def test_duplicate_id() -> None:
    """дубликат id"""
    catalog = AviationCatalog()
    catalog.add(make_part())

    with pytest.raises(DuplicateIdError):
        catalog.add(make_part())


def test_search() -> None:
    """поиск по категории и имени"""
    catalog = AviationCatalog()
    part = make_part()
    catalog.add(part)

    assert catalog.find_by_category("корпус") == [part]
    assert catalog.find_by_name("КРЫЛО") == [part]


def test_iteration() -> None:
    """порядок итерации"""
    catalog = AviationCatalog()
    first = make_part("2")
    second = make_part("1")

    catalog.add(first)
    catalog.add(second)

    assert list(catalog) == [first, second]


def test_json_round_trip(tmp_path) -> None:
    """round trip json"""
    filename = str(tmp_path / "parts.json")
    catalog = AviationCatalog()
    catalog.add(make_part())
    catalog.save(filename)

    new_catalog = AviationCatalog()
    new_catalog.load(filename)

    assert list(catalog) == list(new_catalog)


def test_json_errors(tmp_path) -> None:
    """поврежденный json и неизвестная версия"""
    filename = tmp_path / "parts.json"
    catalog = AviationCatalog()

    filename.write_text("{", encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        catalog.load(str(filename))

    filename.write_text('{"format_version": 999, "items": []}', encoding="utf-8")
    with pytest.raises(UnsupportedVersionError):
        catalog.load(str(filename))


def test_no_partial_load(tmp_path) -> None:
    """проверка отсутствия частичного изменения после ошибки загрузки"""
    filename = tmp_path / "parts.json"
    catalog = AviationCatalog()
    catalog.add(make_part())

    data = {
        "format_version": 1,
        "items": [
            {
                "id": "2",
                "name": "турбина",
                "category": "двигатель",
                "year": 2020,
                "weight": 150.5,
                "material": "алюминий"
            },
            {"id": "3"}
        ]
    }

    with open(filename, "w", encoding="utf-8") as file:
        dump(data, file)

    with pytest.raises(CorruptedFileError):
        catalog.load(str(filename))

    assert list(catalog) == [make_part()]
