from .catalog import AviationCatalog
from .part import AviationPart


def main() -> None:
    """запускает каталог авиационных деталей"""
    catalog = AviationCatalog()
    part = AviationPart("123", "крыло", "корпус", 2020, 150.5, "алюминий")
    catalog.add(part)

    for item in catalog:
        print(item.name)


if __name__ == "__main__":
    main()
