from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from magnit.application import constants


@dataclass
class Contragent:
    """Контрагент (организация)"""
    contragent_type: constants.ContragentType
    inn: str
    kpp: Optional[str]
    name: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    polygons: List[Polygon] = field(default_factory=list)
    employees: List[User] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class Polygon:
    """Полигон"""
    name: str
    full_name: str
    owner: Contragent
    phone_number: Optional[str] = None
    address: Optional[str] = None
    employees: List[User] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class SecondaryRoute:
    """Связь полигонов первого и второго плеча"""
    source_polygon: Polygon
    receiver_polygon: Polygon


@dataclass
class User:
    """Пользователь"""
    phone_number: int
    password: str
    user_role: constants.UserRole
    first_name: str
    last_name: str
    second_name: Optional[str] = None
    user_position: Optional[str] = None
    contragent: Optional[Contragent] = None
    polygon: Optional[Polygon] = None
    e_mail: Optional[str] = None
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        return '%s %s %s' % (
            self.last_name,
            self.first_name,
            self.second_name,
        )


@dataclass
class VehicleModel:
    """Модель транспортного средства"""
    name: str
    id: Optional[int] = None


@dataclass
class Vehicle:
    """Транспортное средство"""
    model: VehicleModel
    reg_number: str
    sts_number: str
    vehicle_type: constants.VehicleType
    tara: int
    max_weight: int
    production_year: int
    body_volume: Optional[int] = None
    compress_ratio: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Permission:
    """Разрешение на допуск на полигон"""
    contragent: Contragent
    expired_at: datetime
    operator: User
    permit: Permit
    is_tonar: bool = False
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None

    @property
    def is_valid(self) -> bool:
        return self.expired_at >= datetime.utcnow()


@dataclass
class Permit:
    """Пропуск"""
    number: int
    vehicle: Vehicle
    permissions: List[Permission] = field(default_factory=list)
    id: Optional[int] = None


@dataclass
class Visit:
    """Визит на полигон"""
    operator_in: User
    permission: Permission
    polygon: Polygon
    weight_in: int
    checked_in: datetime = field(default_factory=datetime.utcnow)
    checked_out: Optional[datetime] = None
    operator_out: Optional[User] = None
    weight_out: Optional[int] = None
    driver: Optional[User] = None
    destination: Optional[Polygon] = None
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    id: Optional[int] = None

    @property
    def status(self) -> constants.VisitStatus:
        """Статус визита"""
        if self.operator_out is None:
            return constants.VisitStatus.IN

        return constants.VisitStatus.OUT

    @property
    def invoice_num(self):
        """Номер документа о визите"""
        p = self.polygon.name[:3].upper()
        m = constants.months_translator.get(self.checked_in.month)
        y = self.checked_in.year
        num = self.id
        return f'{p}-{m}.{y}-{num}'  # ЛЕН-МАЙ.2022-23

    @property
    def invoice_date(self) -> str:
        """Дата документа о визите"""
        return self.checked_in.strftime("%d/%m/%Y %H:%M")

    @property
    def netto(self) -> int:
        """Масса груза"""
        assert self.weight_out is not None, 'Visit is active. ' \
                                            'Finish visit before call.'
        return abs(self.weight_in - self.weight_out)

    @property
    def tara(self) -> int:
        """Масса пустого"""
        assert self.weight_out is not None, 'Visit is active. ' \
                                            'Finish visit before call.'
        return min(self.weight_in, self.weight_out)

    @property
    def brutto(self) -> int:
        """Масса с грузом"""
        assert self.weight_out is not None, 'Visit is active. ' \
                                            'Finish visit before call.'
        return max(self.weight_in, self.weight_out)


@dataclass
class DocsLog:
    title: str
    type: constants.DocType
    user: User
    created_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None
