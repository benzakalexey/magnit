import re

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import interfaces, entities, errors, constants

from magnit.application.dtos_layer import UserAddInfo
from magnit.application.services.auth import hash_it
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
    def add_user(self, user_info: UserAddInfo):

        cleaned_login = re.sub('[^0-9]+', '', user_info.phone_number)

        if not cleaned_login.isalnum():
            raise errors.AuthorizationError()

        if len(cleaned_login) < 10:
            raise errors.AuthorizationError()

        cleaned_login = cleaned_login[-10:]

        phone_number = int(cleaned_login)

        password = hash_it(user_info.password)

        user_role = user_info.user_role
        first_name = user_info.first_name
        last_name = user_info.last_name

        user = entities.User(
            phone_number=phone_number,
            password=password,
            user_role=user_role,
            first_name=first_name,
            last_name=last_name,
        )
        self.users_repo.add(user)
        self.users_repo.save()
