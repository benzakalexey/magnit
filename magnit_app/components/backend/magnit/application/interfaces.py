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
