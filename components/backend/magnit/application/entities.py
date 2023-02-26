from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from magnit.application import constants


@dataclass
class User:
    """Пользователь"""
    phone: int
    password_hash: str
    user_role: constants.UserRole
    is_staff: bool
    is_active: bool
    surname: str
    name: str
    patronymic: Optional[str] = None
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        if self.patronymic is None:
            return '%s %s' % (
                self.surname,
                self.name,
            )
        return '%s %s %s' % (
            self.surname,
            self.name,
            self.patronymic,
        )


@dataclass
class Polygon:
    """Полигон"""
    name: str
    details: List[PolygonDetails] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class Staff:
    """Персонал"""
    user: User
    role: constants.UserRole
    polygon: Optional[Polygon] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class Driver:
    """Водитель"""
    surname: str
    name: str
    details: List[DriverDetails] = field(default_factory=list)
    patronymic: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Partner:
    """Контрагент (организация)"""
    inn: str
    name: str
    short_name: str
    details: List[PartnerDetails] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class Contract:
    """Договор"""
    number: str
    sender: Partner
    'Отправитель'

    receiver: Partner
    'Получатель'

    destination: Polygon
    'Полигон назначения'

    valid_from: datetime
    carrier: Optional[Partner] = None
    'Перевозчик'

    departure_point: Optional[Polygon] = None
    'Полигон отправления'

    valid_to: Optional[datetime] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class DriverDetails:
    """Данные о водителе"""
    driver: Driver
    license: str
    employer: Partner
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class PartnerDetails:
    partner: Partner
    kpp: str
    address: str
    phone: Optional[str]
    valid_from: datetime
    valid_to: Optional[datetime]
    id: Optional[int] = None


@dataclass
class PolygonDetails:
    """Данные о полигоне"""
    polygon: Polygon
    address: str
    valid_from: datetime
    valid_to: Optional[datetime] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class TruckModel:
    """Модель транспортного средства"""
    name: str
    id: Optional[int] = None


@dataclass
class Truck:
    """Транспортное средство"""
    model: TruckModel
    reg_number: str
    passport: str
    type: constants.TruckType
    tara: int
    max_weight: int
    production_year: int
    body_volume: Optional[int] = None
    compress_ratio: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Trailer:
    """Прицеп"""
    model: str
    reg_number: str
    tara: int
    id: Optional[int] = None


@dataclass
class Permission:
    """Допуск на полигон"""
    owner: Partner
    expired_at: datetime
    permit: Permit
    is_active: bool = True  # Валидность допуска
    is_tonar: bool = False  # Тип допуска
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None

    @property
    def is_valid(self) -> bool:
        return self.expired_at >= datetime.utcnow()


@dataclass
class Permit:
    """Пропуск"""
    number: int
    truck: Truck
    permissions: List[Permission] = field(default_factory=list)
    id: Optional[int] = None

    @property
    def permission(self) -> Optional[Permission]:
        """Актуальный допуск"""
        if len(self.permissions) == 0:
            return None

        return self.permissions[0]


@dataclass
class Visit:
    """Визит на полигон"""
    invoice_num: str
    weight_in: int
    operator_in: User
    permission: Permission
    polygon: Polygon
    checked_in: datetime = field(default_factory=datetime.utcnow)
    checked_out: Optional[datetime] = None
    operator_out: Optional[User] = None
    weight_out: Optional[int] = None
    driver: Optional[User] = None
    contract: Optional[Contract] = None
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    id: Optional[int] = None

    @property
    def status(self) -> constants.VisitStatus:
        """Статус визита"""
        if not self.is_deleted:
            if self.operator_out is None:
                return constants.VisitStatus.IN

            return constants.VisitStatus.OUT

        return constants.VisitStatus.DEL

    # @property
    # def invoice_num(self):
    #     """Номер документа о визите"""
    #     p = self.polygon.name[:3].upper()
    #     m = constants.months_translator.get(self.checked_in.month)
    #     y = self.checked_in.year
    #     num = self.id
    #     return f'{p}-{m}.{y}-{num}'  # ЛЕН-МАЙ.2022-23
    # TODO create util for generate invoice_num

    @property
    def invoice_date(self) -> str:
        """Дата документа о визите"""
        return self.checked_in.strftime("%d/%m/%Y %H:%M")

    @property
    def netto(self) -> int:
        """Масса груза"""
        return abs(
            self.weight_in - self.weight_out
        ) if self.weight_out else None

    @property
    def tara(self) -> int:
        """Масса пустого"""
        if self.permission.is_tonar:
            return self.weight_in
        else:
            return self.weight_out

    @property
    def brutto(self) -> int:
        """Масса с грузом"""
        if not self.permission.is_tonar:
            return self.weight_in
        else:
            return self.weight_out
