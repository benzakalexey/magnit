from typing import List

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import constants, entities, errors, interfaces
from magnit.application.dto import TruckInfo, TruckModelInfo
from magnit.application.services.join_point import join_point


@component
class TruckModel:
    """
        Класс Модели автомобилей (справочник)
    """
    truck_models_repo: interfaces.TruckModelRepo

    @join_point
    @validate_arguments
    def get_by_id(self, truck_model_id: conint(gt=0)) -> entities.TruckModel:
        truck_model = self.truck_models_repo.get_by_id(truck_model_id)
        if truck_model is None:
            raise errors.TruckModelIDNotExistError(
                truck_model_id=truck_model_id)

        return truck_model

    @join_point
    @validate_with_dto
    def add_model(self, truck_models_info: TruckModelInfo):
        truck_model = entities.TruckModel(name=truck_models_info.name)
        self.truck_models_repo.add(truck_model)
        self.truck_models_repo.save()


@component
class Truck:
    """
        Класс Автомобили
    """
    trucks_repo: interfaces.TruckRepo
    truck_models_repo: interfaces.TruckModelRepo
    trailer_repo: interfaces.TrailerRepo
    permit_repo: interfaces.PermitRepo
    partner_repo: interfaces.PartnerRepo
    user_repo: interfaces.UserRepo

    @join_point
    @validate_arguments
    def get_by_id(self, truck_id: conint(gt=0)) -> entities.Truck:
        t = self.trucks_repo.get_by_id(truck_id)
        if t is None:
            raise errors.TruckIDNotExistError(truck_id=truck_id)

        return t

    @join_point
    def get_all_models(self) -> List[entities.TruckModel]:
        return self.truck_models_repo.get_all()

    @join_point
    def get_types(self):
        return constants.TruckType

    @join_point
    def get_trailers(self):
        return self.trailer_repo.get_all()

    @join_point
    def get_all(self) -> List[entities.Truck]:
        trucks = self.trucks_repo.get_all()
        return trucks

    @join_point
    @validate_with_dto
    def add_truck(self, truck_info: TruckInfo):
        model = self.truck_models_repo.get_by_id(truck_info.model)
        if model is None:
            raise errors.TruckModelIDNotExistError(
                truck_model_id=truck_info.model)

        truck = entities.Truck(
            reg_number=truck_info.reg_number,
            model=model,
            type=truck_info.type,
            passport='',
            tara=truck_info.tara,
            max_weight=truck_info.max_weight,
            production_year=truck_info.production_year,
            permit=None,
        )
        self.trucks_repo.add(truck)
        self.trucks_repo.save()

        permit_number = self.permit_repo.get_max_num() + 1

        permit = entities.Permit(
            number=permit_number,
            truck=truck,
        )
        partner = self.partner_repo.get_by_id(truck_info.carrier)
        if partner is None:
            raise errors.PartnerIDNotExistError(partner_id=truck_info.carrier)

        trailer = self.trailer_repo.get_by_id(truck_info.trailer)

        operator = self.user_repo.get_by_id(truck_info.user_id)
        permission = entities.Permission(
            owner=partner,
            expired_at=truck_info.permit_exp,
            trailer=trailer,
            permit=permit,
            is_tonar=truck_info.is_tonar,
            added_by=operator,
        )
        permit.permissions.append(permission)
        self.permit_repo.save()
