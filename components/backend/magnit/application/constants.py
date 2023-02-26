from enum import Enum


class UserRole(Enum):
    POLYGON_CHIEF = 'Начальник полигона'
    CONTROLLER = 'Контролер'
    SUPERVISOR = 'Супервайзер'


class PartnerType(Enum):
    """Тип организации"""

    PRIMARY_ROUTE = 'Перевозчик 1 плечо'
    SECONDARY_ROUTE = 'Перевозчик 2 плечо'
    POLYGON_OWNER = 'Владелец полигона'
    PRINCIPAL = 'Заказчик'


class TruckType(Enum):
    """Тип автомобиля"""

    BUNKER_CARRIER = "БУНКЕРОВОЗ"
    CAR = "ЛЕГКОВОЙ АВТОМОБИЛЬ"
    CARGO = "ГРУЗОВОЙ"
    CARGO_OTHER = "ГРУЗОВОЙ ПРОЧИЕ"
    DUMP_TRUCK = "ГРУЗОВОЙ САМОСВАЛ"
    GARBAGE_TRUCK = "МУСОРОВОЗ"
    MULTILIFT = "МУЛЬТИЛИФТ"
    SCRAP_TRUCK = "ЛОМОВОЗ"
    SPECIALIZED = "СПЕЦИАЛИЗИРОВАННЫЙ АВТОМОБИЛЬ"
    SPECIALIZED_OTHER = "ПРОЧИЕ СПЕЦИАЛИЗИРОВАННЫЕ"
    TIPPER = "САМОСВАЛ"
    TRACTOR = "ТЯГАЧ"


class PermitStatus(Enum):
    """Статус пропуска"""

    EXPIRED = 0
    "Просрочен"

    VALID = 1
    "Действителен"


class VisitStatus(Enum):
    """Статус визита"""
    IN = 0
    "На полигоне"

    OUT = 1
    "Выехал"

    DEL = 2
    "Удален"


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
