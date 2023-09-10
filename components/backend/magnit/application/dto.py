from datetime import datetime
from typing import Optional

from classic.app import DTO
from pydantic import conint

from magnit.application import constants


class UserAddInfo(DTO):
    phone_number: str
    password: str
    user_role: constants.UserRole
    first_name: str
    last_name: str


class PartnerInfo(DTO):
    name: str
    inn: str
    kpp: Optional[str]
    contragent_type: constants.PartnerType
    address: Optional[str]
    phone_number: Optional[str]


class PolygonInfo(DTO):
    name: str
    location: Optional[str] = None
    owner_id: conint(gt=0)
    phone_number: Optional[str] = None
    address: Optional[str] = None


class TruckModelInfo(DTO):
    name: str


class TruckInfo(DTO):
    user_id: conint(gt=0)
    is_tonar: bool
    body_volume: Optional[conint(gt=0)]
    carrier: conint(gt=0)
    compress_ratio: Optional[conint(gt=0)]
    max_weight: conint(gt=0)
    model: conint(gt=0)
    permit_exp: datetime
    production_year: Optional[conint(gt=0)]
    reg_number: str
    tara: conint(gt=0)
    trailer: Optional[conint(gt=0)]
    type: constants.TruckType


class SecondaryRouteInfo(DTO):
    source_polygon_id: conint(gt=0)
    receiver_polygon_id: conint(gt=0)


class PermitInfo(DTO):
    number: conint(gt=0)
    truck_id: conint(gt=0)


class PermitLogInfo(DTO):
    permit_id: conint(gt=0)
    user_id: conint(gt=0)
    # operation_type: constants.PermitOperationType
    valid_to: datetime


class VisitInInfo(DTO):
    permission_id: Optional[conint(gt=0)] = None
    polygon_id: Optional[conint(gt=0)] = None
    service_contract_id: Optional[conint(gt=0)] = None
    truck_number: Optional[str] = None
    user_id: int
    weight: conint(gt=0)


class VisitOutInfo(DTO):
    weight: conint(gt=0)
    user_id: int
    visit_id: int
    driver_id: Optional[conint(gt=0)] = None
    contract_id: Optional[conint(gt=0)] = None


class TonarUpdateInfo(DTO):
    contract_id: Optional[conint(gt=0)] = None
    driver_id: Optional[conint(gt=0)] = None
    user_id: int
    visit_id: int
    weight_in: conint(gt=0)
    weight_out: Optional[conint(gt=0)] = None


class TonarXls(DTO):
    weight_out: conint(gt=0)
    invoice_num: str
    driver: str
    destination: str


class TonarXlsError(DTO):
    row: conint(gt=0)
    field: str
    value: str
    comment: str


class DocLogInfo(DTO):
    visit_id: conint(gt=0)
    user_id: conint(gt=0)
    doc_type: constants.DocType
    doc_name: str
