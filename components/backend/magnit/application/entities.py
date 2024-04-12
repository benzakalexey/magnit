from __future__ import annotations

import decimal
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from magnit.application import constants


@dataclass
class User:
    """Пользователь"""
    phone: int
    password_hash: str
    is_staff: bool
    is_active: bool
    surname: str
    name: str
    patronymic: Optional[str] = None
    staff: Optional[Staff] = None
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        if self.patronymic is None:
            return '%s %s' % (
                self.surname,
                self.name,
            )
        return '%s %s %s' % (
            self.surname,
            self.name,
            self.patronymic,
        )


@dataclass
class Polygon:
    """Полигон"""
    name: str
    details: List[PolygonDetails] = field(default_factory=list)
    id: Optional[int] = None

    def get_details(
            self,
            on_date: datetime = datetime.utcnow(),
    ) -> Optional[PolygonDetails]:
        for d in self.details:
            if on_date >= d.valid_from:
                if d.valid_to is None or d.valid_to >= on_date:
                    return d

        return None


@dataclass
class Staff:
    """Персонал"""
    user: User
    role: constants.UserRole
    polygon: Optional[Polygon] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class Driver:
    """Водитель"""
    surname: str
    name: str
    details: List[DriverDetails] = field(default_factory=list)
    patronymic: Optional[str] = None
    id: Optional[int] = None

    @property
    def full_name(self) -> str:
        if self.patronymic is None:
            return '%s %s' % (
                self.surname,
                self.name,
            )
        return '%s %s %s' % (
            self.surname,
            self.name,
            self.patronymic,
        )


@dataclass
class Partner:
    """Контрагент (организация)"""
    inn: str
    ogrn: str
    name: str
    short_name: str
    details: List[PartnerDetails] = field(default_factory=list)
    id: Optional[int] = None

    def get_details(self, on_date: datetime) -> Optional[PartnerDetails]:
        for d in self.details:
            if on_date >= d.valid_from:
                if d.valid_to is None or d.valid_to >= on_date:
                    return d

        return None

    def get_full_name(self, on_date: datetime) -> str:
        return f'{self.name}, ' \
               f'ИНН: {self.inn}, ' \
               f'Адрес: ' \
               f'{self.get_details(on_date).address}'


@dataclass
class PartnerDetails:
    partner: Partner
    valid_from: datetime

    kpp: str
    "КПП"

    address: str
    "Адрес"

    phone: Optional[str]
    "Телефон"

    bank: Optional[str] = None
    "Банк"

    settlement_account: Optional[str] = None
    "Расчетный счет"

    correspondent_account: Optional[str] = None
    "Корреспондентский счет"

    e_mail: Optional[str] = None
    "Электронная почта"

    valid_to: Optional[datetime] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class Contract:
    """Договор"""
    number: str
    valid_from: datetime

    sender: Partner
    'Отправитель'

    receiver: Partner
    'Получатель'

    destination: Polygon
    'Полигон назначения'

    carrier: Optional[Partner] = None
    'Перевозчик'

    departure_point: Optional[Polygon] = None
    'Полигон отправления'

    valid_to: Optional[datetime] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class DriverDetails:
    """Данные о водителе"""
    driver: Driver
    license: str
    employer: Partner
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class PolygonDetails:
    """Данные о полигоне"""
    polygon: Polygon
    address: str
    scale_accuracy: int
    valid_from: datetime = field(default_factory=datetime.utcnow)
    valid_to: Optional[datetime] = None
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None


@dataclass
class TruckModel:
    """Модель транспортного средства"""
    name: str
    id: Optional[int] = None


@dataclass
class Truck:
    """Транспортное средство"""
    model: TruckModel
    permit: Optional[Permit]
    reg_number: str
    passport: str
    type: constants.TruckType
    tara: int
    max_weight: int
    production_year: int
    body_volume: Optional[int] = None
    compress_ratio: Optional[int] = None
    id: Optional[int] = None


@dataclass
class Trailer:
    """Прицеп"""
    model: str
    reg_number: str
    tara: int
    id: Optional[int] = None


@dataclass
class Permission:
    """Допуск на полигон"""
    owner: Partner
    expired_at: datetime
    permit: Permit
    trailer: Optional[Trailer] = None
    is_active: bool = True  # Валидность допуска
    is_tonar: bool = False  # Тип допуска
    added_by: Optional[User] = None
    added_at: datetime = field(default_factory=datetime.utcnow)
    id: Optional[int] = None

    @property
    def is_valid(self) -> bool:
        return self.expired_at >= datetime.utcnow()

    @property
    def truck_description(self) -> str:
        if self.trailer:
            max_netto = (self.permit.truck.max_weight -
                         self.permit.truck.tara - self.trailer.tara) / 1000
            return f'{self.permit.truck.type.value.capitalize()} ' \
                   f'{self.permit.truck.model.name.split()[0]}, ' \
                   f'Прицеп: {self.trailer.model} ' \
                   f'{self.permit.truck.body_volume} м³, ' \
                   f'{max_netto} тонн'
        else:
            max_netto = (self.permit.truck.max_weight -
                         self.permit.truck.tara) / 1000
            return f'{self.permit.truck.type.value.capitalize()} ' \
                   f'{self.permit.truck.model.name.split()[0]}, ' \
                   f'{self.permit.truck.body_volume} м³, ' \
                   f'{max_netto} тонн'

    @property
    def truck_number(self) -> str:
        if self.trailer:
            return f'{self.permit.truck.reg_number} ' \
                   f'Прицеп: {self.trailer.reg_number}'
        else:
            return f'{self.permit.truck.reg_number}'


@dataclass
class Permit:
    """Пропуск"""
    number: int
    truck: Optional[Truck]
    permissions: List[Permission] = field(default_factory=list)
    id: Optional[int] = None

    @property
    def permission(self) -> Optional[Permission]:
        """Актуальный допуск"""
        if len(self.permissions) == 0:
            return None

        return self.permissions[0]


@dataclass
class Visit:
    """Визит на полигон"""
    weight_in: int
    operator_in: User
    permission: Permission
    polygon: Polygon
    invoice_num: str = None
    checked_in: datetime = field(default_factory=datetime.utcnow)
    checked_out: Optional[datetime] = None
    operator_out: Optional[User] = None
    weight_out: Optional[int] = None
    driver: Optional[Driver] = None
    contract: Optional[Contract] = None
    is_deleted: Optional[bool] = False
    delete_reason: Optional[str] = None
    frozen: bool = False
    id: Optional[int] = None

    @property
    def status(self) -> constants.VisitStatus:
        """Статус визита"""
        if not self.is_deleted:
            if self.operator_out is None:
                return constants.VisitStatus.IN

            return constants.VisitStatus.OUT

        return constants.VisitStatus.DEL

    def generate_invoice(self):
        """Номер документа о визите"""
        p = self.polygon.name[:3].upper()
        m = constants.months_translator.get(self.checked_in.month)
        y = self.checked_in.year
        num = self.id
        self.invoice_num = f'{p}-{m}.{y}-{num}'

    @property
    def invoice_date(self) -> str:
        """Дата документа о визите"""
        return self.checked_in.strftime("%d/%m/%Y %H:%M")

    @property
    def netto(self) -> int:
        """Масса груза"""
        return abs(self.weight_in -
                   self.weight_out) if self.weight_out else None

    @property
    def tara(self) -> int:
        """Масса пустого или масса ТС если автомобиль не выехал"""
        if self.permission.is_tonar:
            return self.weight_in
        else:
            return self.weight_out or self.permission.permit.truck.tara

    @property
    def brutto(self) -> int:
        """Масса с грузом"""
        if not self.permission.is_tonar:
            return self.weight_in
        else:
            return self.weight_out


@dataclass
class WasteCatalog:
    """Федеральный каталог классификации отходов."""

    name: str
    """Наименование отхода по ФККО"""

    code: str
    """Код отхода по ФККО"""

    hazard_class: str
    """Класс опасности отхода"""

    id: Optional[int] = None


@dataclass
class ContractService:
    """Услуга по договору на оказание услуг."""

    name: str
    """Наименование услуги"""

    type: constants.ServiceContractType
    """Тип услуги"""

    source_id: Optional[int] = None
    """ИД номенклатуры  в 1С"""

    id: Optional[int] = None


@dataclass
class ServicePrice:
    """Прайс на услуги."""

    contract_service: ContractService
    """Услуга"""

    price: decimal.Decimal
    """Цена"""

    valid_from: datetime
    """Действует с"""

    valid_to: Optional[datetime] = None
    """Действует до"""

    id: Optional[int] = None


@dataclass
class ExecutorStorageArea:
    """Площадки накопления Исполнителя по договору на оказание услуг."""

    polygon: Polygon
    """Полигон"""

    contract: 'ServiceContract'
    """Договор на оказание услуг"""

    id: Optional[int] = None


@dataclass
class ServiceContract:
    """Договор на оказание услуг."""

    number: str
    """Номер"""

    valid_from: datetime
    """Действует с"""

    valid_to: datetime
    """Действует до"""

    permit: Permit
    """Пропуск"""

    contract_service: ContractService
    """Услуга"""

    tariff: decimal.Decimal
    """Тариф, руб./тонн"""

    total_cost: decimal.Decimal
    """Стоимость договора"""

    balance_limit: decimal.Decimal
    """Лимит по договору"""

    # Исполнитель
    executor: Partner
    """Исполнитель"""

    executor_person: str
    """Представитель Исполнителя"""

    executor_acts_basis: str
    """Основания для полномочий Исполнителя"""

    executor_storage_areas: List[Polygon]
    """Площадки накопления"""

    # Заказчик
    customer: Partner
    """Заказчик"""

    customer_person: str
    """Представитель Заказчика"""

    customer_acts_basis: str
    """Основания для полномочий Заказчика"""

    id: Optional[int] = None


@dataclass
class ServiceContractVisit:
    """Визит по Договору на оказание услуг."""

    contract: ServiceContract
    """ИД договора"""

    polygon: Polygon
    """ИД полигона"""

    truck_number: str
    """Номер ТС"""

    # Въезд
    operator_in: User
    """ИД оператора въезда"""

    weight_in: int
    """Вес въезда"""

    checked_in: datetime = field(default_factory=datetime.utcnow)
    """Время въезда"""

    # Выезд
    checked_out: Optional[datetime] = None
    """Время выезда"""

    operator_out: Optional[User] = None
    """ИД оператора выезда"""

    weight_out: Optional[int] = None
    """Вес выезда"""

    invoice_num: Optional[str] = None
    """Номер накладной"""

    id: Optional[int] = None

    def generate_invoice(self):
        """Номер документа о визите"""
        p = self.polygon.name[:3].upper()
        m = constants.months_translator.get(self.checked_in.month)
        y = self.checked_in.year
        num = self.id
        service_type = self.contract.contract_service.type.value
        self.invoice_num = f'{p}-{m}.{y}-{num}-{service_type}'
