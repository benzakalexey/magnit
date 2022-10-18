from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from magnit.adapters.database import constants


@dataclass
class UserGroup:
    name: str
    id: Optional[int] = None


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
    user_group: UserGroup
    contragent: Contragent
    user_position: str
    second_name: Optional[str] = None
    polygon: Optional[Polygon] = None  #
    e_mail: Optional[str] = None
    phone_number: Optional[str] = None
    id: Optional[int] = None


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
    number: str
    operator: User
    vehicle: Vehicle
    contragent: Contragent
    valid_from: datetime
    valid_to: datetime
    created_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


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
    invoice_num: str
    operator_in: User
    weighted_in: int
    driver: Optional[User] = None
    operator_out: Optional[User] = None
    weighted_out: Optional[int] = None
    checked_in: Optional[datetime] = None
    checked_out: Optional[datetime] = None
    destination: Optional[Polygon] = None
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    id: Optional[int] = None


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
    weighted_in: int
    weighted_out: int
    driver: User
    destination: Polygon
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    id: Optional[int] = None
