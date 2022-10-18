from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import interfaces, entities, errors

from magnit.application.dtos_layer import UserInfo, UserGroupInfo
from magnit.application.services.join_point import join_point


@component
class User:
    users_repo: interfaces.UserRepo
    contragents_repo: interfaces.ContragentRepo
    user_groups_repo: interfaces.UserGroupRepo
    polygons_repo: interfaces.PolygonRepo

    @join_point
    @validate_arguments
    def get_by_id(self, user_id: conint(gt=0)) -> entities.User:
        return self.users_repo.get_by_id(user_id)

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

        user_group = self.user_groups_repo.get_by_id(user_info.user_group_id)
        if user_group is None:
            raise errors.UserGroupIDNotExistError(
                user_group_id=user_info.user_group_id
            )

        polygon = self.polygons_repo.get_by_id(user_info.polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(polygon_id=user_info.polygon_id)

        if user_info.last_name is None:
            raise errors.UserLastNameIsNoneError()

        user = entities.User(
            login=user_info.login,
            password=user_info.password,
            first_name=user_info.first_name,
            second_name=user_info.second_name,
            last_name=user_info.last_name,
            contragent=contragent,
            user_group=user_group,
            polygon=polygon,
            user_position=user_info.user_position,
        )
        self.users_repo.add(user)
        self.users_repo.save()


@component
class UserGroup:
    """
    Класс Группы пользователей
    """
    user_groups_repo: interfaces.UserGroupRepo

    @join_point
    @validate_arguments
    def get_by_id(self, user_group_id: conint(gt=0)) -> entities.UserGroup:
        return self.user_groups_repo.get_by_id(user_group_id)

    @join_point
    def get_all(self):
        return self.user_groups_repo.get_all()

    @join_point
    @validate_with_dto
    def add_group(self, user_groups_info: UserGroupInfo):
        if user_groups_info.name is None:
            raise errors.UserGroupNameIsNoneError()

        user_group = entities.UserGroup(
            name=user_groups_info.name,
        )
        self.user_groups_repo.add(user_group)
        self.user_groups_repo.save()
