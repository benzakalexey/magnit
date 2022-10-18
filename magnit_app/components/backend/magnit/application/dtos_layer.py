from datetime import datetime
from typing import Optional

from classic.app import DTO
from pydantic import conint, Field

from magnit.adapters.database import constants


class UserInfo(DTO):
    login: str
    password: str
    last_name: str = Field(description='Фамилия')
    first_name: str = Field(description='Имя')
    second_name: Optional[str] = Field(description='Отчество')
    user_group_id: conint(gt=0)
    contragent_id: conint(gt=0)
    polygon_id: Optional[conint(gt=0)]
    user_position: str
    phone_number: Optional[str]
    e_mail: Optional[str]


class UserGroupInfo(DTO):
    name: str


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
    number: str
    operator_id: conint(gt=0)
    vehicle_id: conint(gt=0)
    contragent_id: conint(gt=0)
    valid_from: datetime
    valid_to: datetime


class PermitLogInfo(DTO):
    permit_id: conint(gt=0)
    user_id: conint(gt=0)
    operated_at: datetime
    operation_type: constants.PermitOperationType
    valid_to: datetime
