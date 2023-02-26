from abc import ABC, abstractmethod
from typing import Optional, List

from magnit.application import entities


class UserRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.User]:
        ...

    @abstractmethod
    def get_by_phone(
        self,
        phone: int,
    ) -> Optional[entities.User]:
        """Возвращает пользователя по номеру телефона

        Args:
            phone: 10-значное число номера телефона

        Returns:
            Объект "Пользователь" или None
        """


class StaffRepo(ABC):

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[entities.Staff]:
        """Возвращает сотрудника по id пользователя

        Args:
            user_id:

        Returns:

        """

    @abstractmethod
    def get_all(self) -> List[entities.User]:
        ...

    @abstractmethod
    def add(self, instance: entities.User):
        ...

    @abstractmethod
    def save(self):
        ...


class PartnerRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Partner]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Partner]:
        ...

    @abstractmethod
    def add(self, instance: entities.Partner):
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
    def get_by_id(self, id_: int) -> Optional[entities.PartnerDetails]:
        ...

    # @abstractmethod
    # def get_by_source_polygon(
    #     self,
    #     source_polygon_id: int,
    # ) -> List[entities.Polygon]:
    #     ...

    @abstractmethod
    def get_all(self) -> List[entities.PartnerDetails]:
        ...

    @abstractmethod
    def add(self, instance: entities.PartnerDetails):
        ...

    @abstractmethod
    def save(self):
        ...


class TruckModelRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.TruckModel]:
        """

        :rtype: object
        """
        ...

    @abstractmethod
    def get_all(self) -> List[entities.TruckModel]:
        ...

    @abstractmethod
    def add(self, instance: entities.TruckModel):
        ...

    @abstractmethod
    def save(self):
        ...


class TruckRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[entities.Truck]:
        ...

    @abstractmethod
    def get_all(self) -> List[entities.Truck]:
        ...

    @abstractmethod
    def add(self, instance: entities.Truck):
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
    def get_last_200(
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
