from .part import AviationPart
from .errors import DuplicateIdError, InvalidPartError, PartNotFoundError, CorruptedFileError, UnsupportedVersionError
from collections.abc import Iterator
from json import dump, load, JSONDecodeError
class AviationCatalog:
    """каталог авиационных деталей"""
    def __init__(self) -> None:
        """создает пустой каталог"""
        self._items: dict[str, AviationPart] = {}

    def add(self, item: AviationPart) -> None:
        """добавляет деталь в каталог"""
        if not isinstance(item, AviationPart):
            raise InvalidPartError("неверная авиационная деталь")
        if item.id in self._items:
            raise DuplicateIdError("деталь с таким id уже существует")
        self._items[item.id] = item

    def get(self, item_id: str) -> AviationPart:
        """возвращает деталь по id"""
        if item_id not in self._items:
            raise PartNotFoundError("деталь не найдена")
        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        """удаляет деталь по id"""
        if item_id not in self._items:
            raise PartNotFoundError("деталь не найдена")
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[AviationPart]:
        """ищет детали по категории"""
        result = []
        for item in self._items.values():
            if item.category == category:
                result.append(item)
        return result

    def find_by_name(self, query: str) -> list[AviationPart]:
        """ищет детали по названию"""
        result = []
        for item in self._items.values():
            if query.lower() in item.name.lower():
                result.append(item)
        return result

    def __len__(self) -> int:
        """возвращает количество деталей"""
        return len(self._items)

    def __iter__(self) -> Iterator[AviationPart]:
        """перебирает детали в порядке добавления"""
        return iter(self._items.values())

    def __contains__(self, item_id: str) -> bool:
        """проверяет наличие детали по id"""
        return item_id in self._items

    def save(self, filename: str) -> None:
        """сохраняет каталог в json"""
        items = []

        for item in self._items.values():
            items.append({
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "year": item.year,
                "weight": item.weight,
                "material": item.material
            })

        data = {"format_version": 1, "items": items}

        with open(filename, "w", encoding="utf-8") as file:
            dump(data, file, ensure_ascii=False, indent=4)



    def load(self, filename: str) -> None:
        """загружает каталог из json"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = load(file)
        except (OSError, UnicodeError, JSONDecodeError):
            raise CorruptedFileError("поврежденный файл")

        if not isinstance(data, dict) or "format_version" not in data:
            raise CorruptedFileError("поврежденный файл")

        if data["format_version"] != 1:
            raise UnsupportedVersionError("неподдерживаемая версия формата")

        if not isinstance(data.get("items"), list):
            raise CorruptedFileError("поврежденный файл")
        new_items = {}
        for item_data in data["items"]:
            try:
                part = AviationPart(**item_data)
            except (TypeError, InvalidPartError):
                raise CorruptedFileError("поврежденный файл")
            if part.id in new_items:
                raise CorruptedFileError("поврежденный файл")
            new_items[part.id] = part
        self._items = new_items
    def read_only(self) -> tuple[AviationPart,...]:
        """возвращает детали только для чтения"""
        return tuple(self._items.values())
