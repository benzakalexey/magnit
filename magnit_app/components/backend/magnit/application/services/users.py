from classic.app import validate_with_dto
from classic.components import component

from magnit.application import interfaces

from magnit.application.dtos_layer import UserInfo
from magnit.application.services.join_point import join_point


@component
class User:
    users_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def get_by_id(self, user_info: UserInfo):
        return self.users_repo.get_by_id(user_info.id)
