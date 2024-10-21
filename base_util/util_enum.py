from enum import Enum


class PackType(Enum):
    CODE = 0
    TEST = 1
    RELEASE = 2
    COMMUNITY = 3


class RowStateColor(Enum):
    NORMAL = 0
    ERROR = 1
    WARNING = 2
    CANT_USE = 3


class SettingType(Enum):
    CHECK = 0
    FILE_PICK = 1
    LIST_ENUM = 2
    LINK = 3
