from abc import ABC, abstractmethod
from typing import Optional, List

from magnit.application import entities


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.User]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.User]:
        ...

    @abstractmethod
    def add(self, instance: entities.User):
        ...

    @abstractmethod
    def save(self):
        ...

class UserGroupRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.UserGroup]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.UserGroup]:
        ...

    @abstractmethod
    def add(self, instance: entities.UserGroup):
        ...

    @abstractmethod
    def save(self):
        ...

class ContragentRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Contragent]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Contragent]:
        ...

    @abstractmethod
    def add(self, instance: entities.Contragent):
        ...

    @abstractmethod
    def save(self):
        ...

class PolygonRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Polygon]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Polygon]:
        ...

    @abstractmethod
    def add(self, instance: entities.Polygon):
        ...

    @abstractmethod
    def save(self):
        ...


class SecondaryRouteRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.SecondaryRoute]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.SecondaryRoute]:
        ...

    @abstractmethod
    def add(self, instance: entities.SecondaryRoute):
        ...

    @abstractmethod
    def save(self):
        ...


class VehicleModelRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.VehicleModel]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.VehicleModel]:
        ...

    @abstractmethod
    def add(self, instance: entities.VehicleModel):
        ...

    @abstractmethod
    def save(self):
        ...


class VehicleRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Vehicle]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Vehicle]:
        ...

    @abstractmethod
    def add(self, instance: entities.Vehicle):
        ...

    @abstractmethod
    def save(self):
        ...


class PermitRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Permit]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Permit]:
        ...

    @abstractmethod
    def add(self, instance: entities.Permit):
        ...

    @abstractmethod
    def save(self):
        ...


class PermitLogRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.PermitLog]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.PermitLog]:
        ...

    @abstractmethod
    def add(self, instance: entities.PermitLog):
        ...

    @abstractmethod
    def save(self):
        ...