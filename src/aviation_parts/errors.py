class CatalogError(Exception):
    """общая ошибка каталога"""


class InvalidPartError(CatalogError):
    """неверная авиационная деталь"""


class DuplicateIdError(CatalogError):
    """повторяющийся id"""


class PartNotFoundError(CatalogError):
    """деталь не найдена"""


class UnsupportedVersionError(CatalogError):
    """неподдерживаемая версия формата"""


class CorruptedFileError(CatalogError):
    """поврежденный файл"""
