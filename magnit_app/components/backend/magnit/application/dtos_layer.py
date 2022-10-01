from typing import Optional

from classic.app import DTO
from pydantic import conint

from magnit.adapters.database import constants


class UserInfo(DTO):
    id: conint(gt=0)


class UserGroupInfo(DTO):
    id: Optional[conint(gt=0)]
    name: Optional[str]


class ContragentInfo(DTO):
    id: Optional[conint(gt=0)]
    name: Optional[str]
    inn: Optional[str]
    kpp: Optional[str]
    contragent_type: Optional[constants.ContragentType]
    address: Optional[str]
    phone_number: Optional[str]


class PolygonInfo(DTO):
    id: Optional[conint(gt=0)]
    name: Optional[str]
    full_name: Optional[str]
    owner_id: conint(gt=0)
    phone_number: Optional[str] = None
    address: Optional[str] = None