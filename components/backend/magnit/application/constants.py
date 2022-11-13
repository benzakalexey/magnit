from enum import Enum


class ContragentType(Enum):
    """Тип организации"""

    PRIMARY_ROUTE_TRANSPORTER = 'Перевозчик 1 плечо'
    SECONDARY_ROUTE_TRANSPORTER = 'Перевозчик 2 плечо'
    POLYGON_OWNER = 'Владелец полигона'
    PRINCIPAL = 'Заказчик'


class VehicleType(Enum):
    """Тип автомобиля"""

    GARBAGE = 'Мусоровоз'
    TONAR = 'Тонар'
    BUNKER = 'Бункеровоз'
    SCRAP = 'Ломовоз'


class PermitOperationType(Enum):
    """Тип операции с пропуском"""

    CREATION = 'Создание'
    PROLONGATION = 'Продление'
    CANCELLATION = 'Аннулирование'


class DocType(Enum):
    """Тип документа"""

    PERMIT = 'Пропуск'
    WEIGHING_ACT = 'Акт взвешивания'
    TRANSPORT_INVOICE = 'Транспортная накладная'
    REPORT = 'Отчет по возчикам'


class VisitStatus(Enum):
    IN = 'На полигоне'
    OUT = 'Выехал'


class UserRole(Enum):
    POLYGON_CHIEF = 'Начальник полигона'
    CONTROLLER = 'Контролер'
    SUPERVISOR = 'Супервайзер'
    DRIVER = 'Водитель'


class Monts:
    months = {
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
