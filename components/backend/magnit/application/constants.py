from enum import Enum


class UserRole(Enum):
    POLYGON_CHIEF = 'Начальник полигона'
    CONTROLLER = 'Контролер'
    SUPERVISOR = 'Супервайзер'
    DRIVER = 'Водитель'


class ContragentType(Enum):
    """Тип организации"""

    PRIMARY_ROUTE = 'Перевозчик 1 плечо'
    SECONDARY_ROUTE = 'Перевозчик 2 плечо'
    POLYGON_OWNER = 'Владелец полигона'
    PRINCIPAL = 'Заказчик'


class VehicleType(Enum):
    """Тип автомобиля"""

    BUNKER = 'Бункеровоз'
    GARBAGE = 'Мусоровоз'
    SCRAP = 'Ломовоз'
    TONAR = 'Тонар'


class VisitStatus(Enum):
    """Статус визита"""
    IN = 0
    "На полигоне"

    OUT = 1
    "Выехал"


class DocType(Enum):
    """Тип документа"""

    PERMIT = 'Пропуск'
    WEIGHING_ACT = 'Акт взвешивания'
    TRANSPORT_INVOICE = 'Транспортная накладная'
    REPORT = 'Отчет по возчикам'


months_translator = {
    1: "ЯНВ",
    2: "ФЕВ",
    3: "МАР",
    4: "АПР",
    5: "МАЙ",
    6: "ИЮН",
    7: "ИЮЛ",
    8: "АВГ",
    9: "СЕН",
    10: "ОКТ",
    11: "НОЯ",
    12: "ДЕК",
}
