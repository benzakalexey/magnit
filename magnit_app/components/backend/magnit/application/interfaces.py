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
