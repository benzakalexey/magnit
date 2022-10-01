from classic.app import validate_with_dto
from classic.components import component

from magnit.application import interfaces, entities, errors

from magnit.application.dtos_layer import UserInfo, UserGroupInfo
from magnit.application.services.join_point import join_point


@component
class User:
    users_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def get_by_id(self, user_info: UserInfo) -> entities.User:
        return self.users_repo.get_by_id(user_info.id)

    @join_point
    def get_all(self):
        return self.users_repo.get_all()

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserInfo):
        ...


@component
class UserGroup:
    """
    Класс Группы пользователей
    """
    user_groups_repo: interfaces.UserGroupRepo

    @join_point
    @validate_with_dto
    def get_by_id(self, user_groups_info: UserGroupInfo):
        return self.user_groups_repo.get_by_id(user_groups_info.id)

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
