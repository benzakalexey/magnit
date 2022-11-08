from datetime import datetime
from typing import Optional

from classic.app import DTO
from pydantic import conint, Field

from magnit.application import constants


class UserInfo(DTO):
    login: str
    password: str
    last_name: str = Field(description='Фамилия')
    first_name: str = Field(description='Имя')
    second_name: Optional[str] = Field(description='Отчество')
    user_role: constants.UserRole
    contragent_id: conint(gt=0)
    polygon_id: Optional[conint(gt=0)]
    user_position: str = Field(description='Должность')
    phone_number: Optional[str]
    e_mail: Optional[str]


class ContragentInfo(DTO):
    name: str
    inn: str
    kpp: Optional[str]
    contragent_type: constants.ContragentType
    address: Optional[str]
    phone_number: Optional[str]


class PolygonInfo(DTO):
    name: str
    full_name: str
    owner_id: conint(gt=0)
    phone_number: Optional[str] = None
    address: Optional[str] = None


class VehicleModelInfo(DTO):
    model: str


class VehicleInfo(DTO):
    model_id: conint(gt=0)
    reg_number: str
    pts_number: str
    production_year: Optional[conint(gt=0)]
    vehicle_type: constants.VehicleType
    tara: conint(gt=0)
    max_weight: conint(gt=0)
    body_volume: Optional[conint(gt=0)]
    compress_ratio: Optional[conint(gt=0)]


class SecondaryRouteInfo(DTO):
    source_polygon_id: conint(gt=0)
    receiver_polygon_id: conint(gt=0)


class PermitInfo(DTO):
    operator_id: conint(gt=0)
    vehicle_id: conint(gt=0)
    contragent_id: conint(gt=0)
    valid_from: datetime
    valid_to: datetime


class PermitLogInfo(DTO):
    permit_id: conint(gt=0)
    user_id: conint(gt=0)
    operation_type: constants.PermitOperationType
    valid_to: datetime


class VisitInInfo(DTO):
    permit_id: int
    user_id: int
    weight: conint(gt=0)
    polygon_id: Optional[conint(gt=0)] = None


class VisitOutInfo(DTO):
    weight: conint(gt=0)
    user_id: int
    visit_id: int
    driver_id: Optional[conint(gt=0)] = None
    destination_id: Optional[conint(gt=0)] = None


class DocLogInfo(DTO):
    visit_id: conint(gt=0)
    user_id: conint(gt=0)
    doc_type: constants.DocType
    doc_name: str


class CopyVisitInfo(DTO):
    visit_id: conint(gt=0)
    permit_id: conint(gt=0)
    polygon_id: conint(gt=0)
    weight_in: conint(gt=0)
    weight_out: Optional[conint(gt=0)]
    driver_id: Optional[conint(gt=0)]
    destination_id: Optional[conint(gt=0)]
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
