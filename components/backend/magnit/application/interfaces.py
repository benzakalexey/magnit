from abc import ABC, abstractmethod
from typing import Optional, List

from magnit.application import entities


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.User]:
        ...

    @abstractmethod
    def get_by_phone_number(
        self,
        phone_number: int,
    ) -> Optional[entities.User]:
        ...

    @abstractmethod
    def get_by_contragent(
        self,
        contragent_id: int,
    ) -> List[entities.User]:
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
    def get_receivers_by_source_id(
        self,
        source_id: int,
    ) -> List[entities.Polygon]:
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

    # @abstractmethod
    # def get_by_source_polygon(
    #     self,
    #     source_polygon_id: int,
    # ) -> List[entities.Polygon]:
    #     ...

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
        """

        :rtype: object
        """
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
    def get_by_number(self, number: int) -> Optional[entities.Permit]:
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


class PermissionRepo(ABC):

    @abstractmethod
    def get_last_by_permit_number(
        self,
        number: int,
    ) -> Optional[entities.Permission]:
        """Возвращает последний Допуск по номеру пропуска"""

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Permission]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Permission]:
        ...

    @abstractmethod
    def add(self, instance: entities.Permission):
        ...

    @abstractmethod
    def save(self):
        ...


class VisitRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Visit]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Visit]:
        ...

    @abstractmethod
    def add(self, instance: entities.Visit):
        ...

    @abstractmethod
    def save(self):
        ...

    @abstractmethod
    def get_last_12_hours(
        self,
        polygon_id: int,
    ) -> List[entities.Visit]:
        """Возвращает визиты за последние 12 часов по ИД Полигона.

        Args:
            polygon_id: ИД Полигона

        Returns:
            список Визитов

        """
        ...


class DocLogRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.DocsLog]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.DocsLog]:
        ...

    @abstractmethod
    def add(self, instance: entities.DocsLog):
        ...

    @abstractmethod
    def save(self):
        ...