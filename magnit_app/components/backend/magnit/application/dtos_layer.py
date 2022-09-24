from classic.app import DTO
from pydantic import conint


class UserInfo(DTO):
    id: conint(gt=0)
