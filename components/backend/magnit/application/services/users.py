from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import interfaces, entities, errors, constants

from magnit.application.dtos_layer import UserInfo
from magnit.application.services.join_point import join_point


@component
class User:
    users_repo: interfaces.UserRepo
    contragents_repo: interfaces.ContragentRepo
    polygons_repo: interfaces.PolygonRepo

    @join_point
    @validate_arguments
    def get_by_id(self, user_id: conint(gt=0)) -> entities.User:
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        return user

    @join_point
    def get_all(self):
        return self.users_repo.get_all()

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        contragent = self.contragents_repo.get_by_id(user_info.contragent_id)
        if contragent is None:
            raise errors.ContragentIDNotExistError(
                contragent_id=user_info.contragent_id
            )

        polygon = self.polygons_repo.get_by_id(user_info.polygon_id)
        if user_info.user_role is None:
            raise errors.UserRoleIsNoneError()
        elif user_info.user_role == constants.UserRole.CONTROLLER:
            if polygon is None:
                raise errors.UserPolygonIsNoneError()

        user = entities.User(
            login=user_info.login,
            password=user_info.password,
            first_name=user_info.first_name,
            second_name=user_info.second_name,
            last_name=user_info.last_name,
            contragent=contragent,
            user_role=user_info.user_role,
            polygon=polygon,
            user_position=user_info.user_position,
        )
        self.users_repo.add(user)
        self.users_repo.save()
