from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint
from magnit.application import interfaces, entities, errors
from magnit.application.dtos_layer import VehicleModelInfo, VehicleInfo
from magnit.application.services.join_point import join_point


@component
class VehicleModel:
    """
        Класс Модели автомобилей (справочник)
    """
    vehicle_models_repo: interfaces.VehicleModelRepo

    @join_point
    @validate_arguments
    def get_by_id(self,
                  vehicle_model_id: conint(gt=0)) -> entities.VehicleModel:
        vehicle_model = self.vehicle_models_repo.get_by_id(vehicle_model_id)
        if vehicle_model is None:
            raise errors.VehicleModelIDNotExistError(
                vehicle_model_id=vehicle_model_id
            )

        return vehicle_model

    @join_point
    def get_all(self):
        return self.vehicle_models_repo.get_all()

    @join_point
    @validate_with_dto
    def add_model(self, vehicle_models_info: VehicleModelInfo):
        vehicle_model = entities.VehicleModel(
            name=vehicle_models_info.name,
        )
        self.vehicle_models_repo.add(vehicle_model)
        self.vehicle_models_repo.save()


@component
class Vehicle:
    """
        Класс Автомобили
    """
    vehicles_repo: interfaces.VehicleRepo
    vehicle_models_repo: interfaces.VehicleModelRepo

    @join_point
    @validate_arguments
    def get_by_id(self, vehicle_id: conint(gt=0)) -> entities.Vehicle:
        vehicle = self.vehicles_repo.get_by_id(vehicle_id)
        if vehicle is None:
            raise errors.VehicleIDNotExistError(vehicle_id=vehicle_id)

        return vehicle

    @join_point
    def get_all(self):
        return self.vehicles_repo.get_all()

    @join_point
    @validate_with_dto
    def add_vehicle(self, vehicle_info: VehicleInfo):
        model = self.vehicle_models_repo.get_by_id(vehicle_info.model_id)
        if model is None:
            raise errors.VehicleModelIDNotExistError(
                vehicle_model_id=vehicle_info.model_id
            )

        vehicle = entities.Vehicle(
            reg_number=vehicle_info.reg_number,
            model=model,
            vehicle_type=vehicle_info.vehicle_type,
            sts_number=vehicle_info.sts_number,
            tara=vehicle_info.tara,
            max_weight=vehicle_info.max_weight,
            production_year=vehicle_info.production_year,
        )
        self.vehicles_repo.add(vehicle)
        self.vehicles_repo.save()

        # permit = entities.Permit(
        #     number=permit_info.number,
        #     vehicle=vehicle
        #
        # )
