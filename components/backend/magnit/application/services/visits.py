import logging
from datetime import datetime, timedelta
from random import randint
from typing import Any, Dict, List

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import dto, entities, errors, interfaces
from magnit.application.services.join_point import join_point


@component
class Visit:
    """
    Класс Визиты на полигон
    """
    contract_repo: interfaces.ContractRepo
    service_contract_repo: interfaces.ServiceContractRepo
    service_contract_visit_repo: interfaces.ServiceContractVisitRepo
    driver_repo: interfaces.DriverRepo
    permission_repo: interfaces.PermissionRepo
    permits_repo: interfaces.PermitRepo
    polygons_repo: interfaces.PolygonRepo
    staff_repo: interfaces.StaffRepo
    truck_repo: interfaces.TruckRepo
    users_repo: interfaces.UserRepo
    visits_repo: interfaces.VisitRepo
    tonars_xls_parser: interfaces.ExcelParser

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @join_point
    @validate_arguments
    def get_by_id(self, visit_id: conint(gt=0)) -> entities.Visit:

        print('here')
        visit = self.visits_repo.get_by_id(visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        return visit

    @join_point
    def get_all(self):
        return self.visits_repo.get_all()

    @validate_with_dto
    def create_visit(self, visit_info: dto.VisitInInfo):
        if visit_info.permission_id:
            self._create_permission_visit(visit_info)
        else:
            self._create_service_contract_visit(visit_info)

    @join_point
    def _create_permission_visit(self, visit_info: dto.VisitInInfo):
        permission = self.permission_repo.get_by_id(visit_info.permission_id)
        if permission is None:
            raise errors.PermitIDNotExistError(
                permit_id=visit_info.permission_id)

        staff = self.staff_repo.get_by_user_id(visit_info.user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        if staff.polygon is None:
            raise errors.PolygonIDNotExistError()

        visit = entities.Visit(
            weight_in=visit_info.weight,
            permission=permission,
            operator_in=staff.user,
            polygon=staff.polygon,
        )
        self.visits_repo.add(visit)

        visit.generate_invoice()

        self.visits_repo.save()

    @join_point
    def _create_service_contract_visit(self, visit_info: dto.VisitInInfo):
        contract = self.service_contract_repo.get_by_id(
            visit_info.service_contract_id, )
        if contract is None:
            raise errors.ServiceContractIDNotExistError(
                contract_id=visit_info.service_contract_id, )

        staff = self.staff_repo.get_by_user_id(visit_info.user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        if staff.polygon is None:
            raise errors.PolygonIDNotExistError()

        visit = entities.ServiceContractVisit(
            contract=contract,
            operator_in=staff.user,
            polygon=staff.polygon,
            truck_number=visit_info.truck_number,
            weight_in=visit_info.weight,
        )
        self.service_contract_visit_repo.add(visit)

        visit.generate_invoice()

        self.service_contract_visit_repo.save()

    @join_point
    @validate_with_dto
    def finish_visit(self, visit_info: dto.VisitOutInfo):
        visit = self.visits_repo.get_by_id(visit_info.visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_info.visit_id)

        user = self.users_repo.get_by_id(visit_info.user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=visit_info.user_id)

        visit.operator_out = user
        visit.weight_out = visit_info.weight
        visit.checked_out = datetime.utcnow()
        self._update_if_tonar(visit, visit_info)
        self.visits_repo.save()

    @join_point
    @validate_with_dto
    def update(self, visit_info: dto.TonarUpdateInfo):
        visit = self.visits_repo.get_by_id(visit_info.visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_info.visit_id)

        if visit_info.driver_id:
            driver = self.driver_repo.get_by_id(visit_info.driver_id)
            if driver is None:
                raise errors.UserIDNotExistError(user_id=visit_info.driver_id)

            visit.driver = driver

        if visit_info.contract_id:
            contract = self.contract_repo.get_by_id(visit_info.contract_id)
            if contract is None:
                raise errors.ContractIDNotFound(
                    contract_id=visit_info.contract_id)

            visit.contract = contract

        visit.weight_in = visit_info.weight_in
        visit.weight_out = visit_info.weight_out
        self.visits_repo.save()

    @join_point
    # @validate_with_dto
    def bulk_tonars_update(self, visits_info: List[Dict[str, int]]):
        for v in visits_info:
            visit = self.visits_repo.get_by_id(v.get('id'))
            if visit is None:
                raise errors.VisitIDNotExistError(visit_id=v.get('id'))

            # visit.weight_in = v.get('weight_in')
            visit.weight_out = v.get('weight_out')

        self.visits_repo.save()

    @join_point
    # @validate_with_dto
    def bulk_update(self, visits_info: List[Dict[str, int]]):
        for v in visits_info:
            visit = self.visits_repo.get_by_id(v.get('id'))
            if visit is None:
                raise errors.VisitIDNotExistError(visit_id=v.get('id'))

            visit.weight_in = v.get('weight_in')
            # visit.weight_out = v.get('weight_out')

        self.visits_repo.save()

    @join_point
    # @validate_with_dto
    def update_from_file(self, file):
        visits_info = self.tonars_xls_parser.get_data(file)
        err = self._check_errors_in_export(visits_info)
        if err:
            return err

        for row, v in enumerate(visits_info):
            visit = self.visits_repo.get_by_invoice_num(v.invoice_num)

            surname, name = v.driver.split()
            driver = self.driver_repo.get_by_name(surname, name)

            destination = self.polygons_repo.get_by_name(v.destination)

            contracts = self.contract_repo.get_by_destination_and_departure(
                destination_point_id=destination.id,
                departure_point_id=visit.polygon.id,
            )
            active_contracts = [
                c for c in contracts
                if c.valid_to >= visit.checked_out >= c.valid_from
            ]

            visit.weight_out = v.weight_out
            visit.driver = driver
            visit.contract = active_contracts[0]

        self.visits_repo.save()
        return err

    @join_point
    def _check_errors_in_export(
        self,
        visits_info: List[dto.TonarXls],
    ) -> List[dto.TonarXlsError]:
        err = []
        for row, v in enumerate(visits_info):
            visit = self.visits_repo.get_by_invoice_num(v.invoice_num)
            if visit is None:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Номер ТН',
                        value=v.invoice_num,
                        comment='Визит не найден',
                    ))
                continue

            surname, name = v.driver.split()
            driver = self.driver_repo.get_by_name(surname, name)
            if driver is None:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Водитель',
                        value=v.driver,
                        comment='Водитель не найден',
                    ))

            if visit.weight_in > v.weight_out:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Брутто',
                        value=v.weight_out,
                        comment='Брутто меньше веса въезда',
                    ))

            destination = self.polygons_repo.get_by_name(v.destination)
            if destination is None:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Направление',
                        value=v.destination,
                        comment='Направление не найдено',
                    ))
                continue

            contracts = self.contract_repo.get_by_destination_and_departure(
                destination_point_id=destination.id,
                departure_point_id=visit.polygon.id,
            )
            active_contracts = [
                c for c in contracts
                if c.valid_to >= visit.checked_out >= c.valid_from
            ]
            if not active_contracts:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Направление',
                        value=v.destination,
                        comment='Договор для направления "%s" не найден' %
                        v.destination,
                    ))
            if len(active_contracts) != 1:
                err.append(
                    dto.TonarXlsError(
                        row=row + 2,
                        field='Направление',
                        value=v.destination,
                        comment='Для направления "%s" больше одного договора.'
                        % v.destination,
                    ))

        return err

    def _update_if_tonar(
        self,
        visit: entities.Visit,
        visit_info: dto.VisitOutInfo,
    ):
        if visit.permission.is_tonar is False:
            return

        driver = self.driver_repo.get_by_id(visit_info.driver_id)
        if driver is None:
            raise errors.UserIDNotExistError(user_id=visit_info.driver_id)

        visit.driver = driver

        contract = self.contract_repo.get_by_id(visit_info.contract_id)
        if contract is None:
            raise errors.ContractIDNotFound(contract_id=visit_info.contract_id)

        visit.contract = contract

    @join_point
    @validate_arguments
    def delete_visit(self, visit_id: int, reason: str):
        visit = self.visits_repo.get_by_id(visit_id)
        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        if not reason:
            raise errors.VisitDeleteReasonIsNoneError()

        visit.is_deleted = True
        visit.delete_reason = reason
        self.visits_repo.save()

    @join_point
    @validate_arguments
    def get_on_polygon(self, user_id: int) -> List[entities.Visit]:

        staff = self.staff_repo.get_by_user_id(user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        polygon = staff.polygon
        if polygon is None:
            raise errors.PolygonIDNotExistError(polygon_id=staff.polygon.id)

        return self.visits_repo.get_last_50(polygon.id)

    @join_point
    @validate_arguments
    def get_tonars(
        self,
        user_id: int,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        self.logger.info('\nafter: %s\nbefore: %s', after, before)
        staff = self.staff_repo.get_by_user_id(user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        return self.visits_repo.get_tonars(after, before)

    @join_point
    @validate_arguments
    def get_visits(
        self,
        user_id: int,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        self.logger.info('\nafter: %s\nbefore: %s', after, before)
        return self.visits_repo.get_between(after, before)

    @join_point
    @validate_arguments
    def get_garbage_trucks(
        self,
        user_id: int,
        after: datetime,
        before: datetime,
    ) -> List[entities.Visit]:
        self.logger.info('\nafter: %s\nbefore: %s', after, before)
        staff = self.staff_repo.get_by_user_id(user_id)
        if staff is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        return self.visits_repo.get_garbage_trucks(after, before)

    @join_point
    @validate_arguments
    def get_invoice(self, visit_id: int) -> Dict[str, Any]:
        visit = self.visits_repo.get_by_id(visit_id)

        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        if not visit.permission.is_tonar:
            raise errors.CantCreateNotTonarInvoice()

        cargo_type = 'Остатки сортировки ТКО'
        carrier = visit.contract.carrier.get_full_name(visit.checked_out)
        direction = visit.contract.destination.get_details(visit.checked_out)
        planned_date = visit.checked_out - timedelta(minutes=randint(20, 30))
        receiver = visit.contract.receiver.get_full_name(visit.checked_out)

        return {
            'cargo_type': cargo_type,
            'carrier': carrier,
            'contract': visit.contract.number,
            'date': visit.checked_out,
            'direction': direction.address,
            'driver': visit.driver.full_name,
            'driver_licence': visit.driver.details[0].license,
            'number': visit.invoice_num,
            'planned_date': planned_date,
            'polygon': visit.polygon.get_details(visit.checked_in).address,
            'receiver': receiver,
            'truck': visit.permission.truck_description,
            'truck_number': visit.permission.truck_number,
            'truck_volume': visit.permission.permit.truck.body_volume,
            'truck_weight': visit.permission.permit.truck.tara,
            'volume': visit.permission.permit.truck.body_volume,
        }

    @join_point
    @validate_arguments
    def get_akt(self, visit_id: int) -> Dict[str, Any]:
        visit = self.visits_repo.get_by_id(visit_id)

        if visit is None:
            raise errors.VisitIDNotExistError(visit_id=visit_id)

        carrier = visit.permission.owner.short_name
        permit_number = visit.permission.permit.number
        truck_mark = visit.permission.permit.truck.model.name
        truck_number = visit.permission.truck_number

        return {
            'brutto': visit.brutto,
            'carrier': carrier,
            'date': visit.checked_out,
            'netto': visit.netto,
            'number': visit.invoice_num,
            'permit_number': permit_number,
            'polygon': visit.polygon.name,
            'service_type': 'Транспортирование ТКО (IV-V)',
            'tara': visit.tara,
            'truck_mark': truck_mark,
            'truck_number': truck_number,
        }
