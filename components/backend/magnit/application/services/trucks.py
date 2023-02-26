from classic.app import validate_with_dto
from classic.components import component
from pydantic import validate_arguments, conint
from magnit.application import interfaces, entities, errors
from magnit.application.dtos_layer import truckModelInfo, truckInfo
from magnit.application.services.join_point import join_point


@component
class TruckModel:
    """
        Класс Модели автомобилей (справочник)
    """
    truck_models_repo: interfaces.TruckModelRepo

    @join_point
    @validate_arguments
    def get_by_id(self,
                  truck_model_id: conint(gt=0)) -> entities.TruckModel:
        truck_model = self.truck_models_repo.get_by_id(truck_model_id)
        if truck_model is None:
            raise errors.truckModelIDNotExistError(
                truck_model_id=truck_model_id
            )

        return truck_model

    @join_point
    def get_all(self):
        return self.truck_models_repo.get_all()

    @join_point
    @validate_with_dto
    def add_model(self, truck_models_info: truckModelInfo):
        truck_model = entities.TruckModel(
            name=truck_models_info.name,
        )
        self.truck_models_repo.add(truck_model)
        self.truck_models_repo.save()


@component
class Truck:
    """
        Класс Автомобили
    """
    trucks_repo: interfaces.TruckRepo
    truck_models_repo: interfaces.TruckModelRepo

    @join_point
    @validate_arguments
    def get_by_id(self, truck_id: conint(gt=0)) -> entities.Truck:
        t = self.trucks_repo.get_by_id(truck_id)
        if t is None:
            raise errors.truckIDNotExistError(truck_id=truck_id)

        return t

    @join_point
    def get_all(self):
        return self.trucks_repo.get_all()

    @join_point
    @validate_with_dto
    def add_truck(self, truck_info: truckInfo):
        model = self.truck_models_repo.get_by_id(truck_info.model_id)
        if model is None:
            raise errors.truckModelIDNotExistError(
                truck_model_id=truck_info.model_id
            )

        truck = entities.Truck(
            reg_number=truck_info.reg_number,
            model=model,
            truck_type=truck_info.truck_type,
            sts_number=truck_info.sts_number,
            tara=truck_info.tara,
            max_weight=truck_info.max_weight,
            production_year=truck_info.production_year,
        )
        self.trucks_repo.add(truck)
        self.trucks_repo.save()

        # permit = entities.Permit(
        #     number=permit_info.number,
        #     truck=truck
        #
        # )
