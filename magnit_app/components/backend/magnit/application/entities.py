from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from magnit.application import constants


@dataclass
class Contragent:
    name: str
    inn: str
    kpp: Optional[str]
    contragent_type: constants.ContragentType
    address: Optional[str] = None
    phone_number: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Polygon:
    name: str
    full_name: str
    owner: Contragent
    phone_number: Optional[str] = None
    address: Optional[str] = None
    id: Optional[int] = None


@dataclass
class SecondaryRoute:
    source_polygon: Polygon
    receiver_polygon: Polygon
    id: Optional[int] = None


@dataclass
class User:
    login: str
    password: str
    first_name: str
    last_name: str
    user_role: constants.UserRole
    contragent: Contragent
    user_position: str
    second_name: Optional[str] = None
    polygon: Optional[Polygon] = None  #
    e_mail: Optional[str] = None
    phone_number: Optional[str] = None
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        return '%s %s %s' % (
            self.last_name,
            self.first_name,
            self.second_name,
        )

    @property
    def phone_print(self) -> str:
        ph_num = ''
        if self.phone_number:
            ph_num = self.phone_number
        return ph_num

@dataclass
class VehicleModel:
    model: str
    id: Optional[int] = None


@dataclass
class Vehicle:
    model: VehicleModel
    reg_number: str
    pts_number: str
    vehicle_type: constants.VehicleType
    tara: int
    max_weight: int
    production_year: Optional[int] = None
    body_volume: Optional[int] = None
    compress_ratio: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Permit:
    operator: User
    vehicle: Vehicle
    contragent: Contragent
    valid_from: datetime
    valid_to: datetime
    created_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None

    @property
    def is_tonar(self) -> bool:
        return self.vehicle.vehicle_type == constants.VehicleType.TONAR


@dataclass
class PermitLog:
    permit: Permit
    user: User
    operation_type: constants.PermitOperationType
    valid_to: datetime
    operated_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class Visit:
    permit: Permit
    polygon: Polygon
    operator_in: User
    weight_in: int
    driver: Optional[User] = None
    operator_out: Optional[User] = None
    weight_out: Optional[int] = None
    checked_in: datetime = field(default_factory=datetime.utcnow)
    checked_out: Optional[datetime] = None
    destination: Optional[Polygon] = None
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    id: Optional[int] = None

    @property
    def status(self) -> constants.VisitStatus:
        if self.operator_out is None:
            return constants.VisitStatus.IN

        return constants.VisitStatus.OUT

    @property
    def invoice_num(self):
        p = self.polygon.name[:3].upper()
        m = constants.Monts.months.get(self.checked_in.month)
        y = self.checked_in.year
        num = self.id
        return f'{p}-{m}.{y}-{num}'  # ЛЕН-МАЙ.2022-23

    @property
    def invoice_date(self) -> str:
        return self.checked_in.strftime("%d/%m/%Y %H:%M")

    @property
    def netto(self) -> int:
        """
        :return: Вес груза
        """
        return abs(self.weight_in - self.weight_out)


@dataclass
class DocsLog:
    visit: Visit
    user: User
    doc_type: constants.DocType
    doc_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class CopyVisit:
    visit: Visit
    permit: Permit
    polygon: Polygon
    weight_in: int
    weight_out: int
    driver: User
    destination: Polygon
    id: Optional[int] = None

    @property
    def is_deleted(self):
        return self.visit.is_deleted

    @property
    def delete_reason(self):
        return self.visit.delete_reason

    def reset(self):
        self.permit = self.visit.permit
        self.polygon = self.visit.polygon
        self.weight_in = self.visit.weight_in
        self.weight_out = self.visit.weight_out
        self.driver = self.visit.driver
        self.destination = self.visit.destination
