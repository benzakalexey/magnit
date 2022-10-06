from enum import Enum


class ContragentType(Enum):
    """Тип организации"""

    PRIMARY_ROUTE_TRANSPORTER = 'PRIMARY_ROUTE_TRANSPORTER'
    'Перевозчик 1 плечо'

    SECONDARY_ROUTE_TRANSPORTER = 'SECONDARY_ROUTE_TRANSPORTER'
    'Перевозчик 2 плечо'

    POLYGON_OWNER = 'POLYGON_OWNER'
    'Владелец полигона'

    PRINCIPAL = 'PRINCIPAL'
    'Заказчик'


class VehicleType(Enum):
    """Тип автомобиля"""

    GARBAGE = 'GARBAGE'
    'Мусоровоз'

    TONAR = 'TONAR'
    'Тонар'

    BUNKER = 'BUNKER'
    'Бункеровоз'

    SCRAP = 'SCRAP'
    'Ломовоз'


class PermitOperationType(Enum):
    """Тип операции с пропуском"""

    CREATION = 'CREATION'
    'Создание'

    PROLONGATION = 'PROLONGATION'
    'Продление'

    CANCELLATION = 'CANCELLATION'
    'Аннулирование'


class DocType(Enum):
    """Тип документа"""

    PERMIT = 'PERMIT'
    'Пропуск'

    WEIGHING_ACT = 'WEIGHING_ACT'
    'Акт взвешивания'

    TRANSPORT_INVOICE = 'TRANSPORT_INVOICE'
    'Транспортная накладная'

    REPORT = 'REPORT'
    'Отчет по возчикам'