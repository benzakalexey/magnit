import re
from typing import List

from classic.app import validate_with_dto
from classic.components import component
from pydantic import conint, validate_arguments

from magnit.application import constants, entities, errors, interfaces
from magnit.application.dto import UserAddInfo, UserUpdateInfo
from magnit.application.entities import Staff
from magnit.application.services.auth import hash_it
from magnit.application.services.join_point import join_point


@component
class Driver:
    driver_repo: interfaces.DriverRepo

    @join_point
    @validate_arguments
    def get_by_partner_id(
            self,
            partner_id: conint(gt=0),
    ) -> List[entities.Driver]:
        all_drivers = self.driver_repo.get_all()
        partner_drivers = (d for d in all_drivers
                           if d.details[0].employer.id == partner_id)
        return sorted(partner_drivers, key=lambda x: x.full_name)


@component
class User:
    users_repo: interfaces.UserRepo
    contragents_repo: interfaces.PartnerRepo
    polygons_repo: interfaces.PolygonRepo

    @join_point
    @validate_arguments
    def get_by_id(self, user_id: conint(gt=0)) -> entities.User:
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        return user

    @join_point
    @validate_arguments
    def get_by_contragent(
            self,
            contragent_id: conint(gt=0),
    ) -> List[entities.User]:
        contragent = self.contragents_repo.get_by_id(contragent_id)
        if contragent is None:
            raise errors.PartnerIDNotExistError(contragent_id=contragent_id)

        return [
            u for u in contragent.employees
            if u.role == constants.UserRole.DRIVER
        ]

    @join_point
    @validate_arguments
    def get_user_roles(self):
        return constants.UserRole

    @join_point
    def get_all(self):
        users = self.users_repo.get_all()
        users.sort(key=lambda a: a.full_name)
        return users

    @join_point
    @validate_with_dto
    def add_user(self, user_info: UserAddInfo):

        cleaned_login = re.sub('[^0-9]+', '', user_info.phone)

        if not cleaned_login.isalnum():
            raise errors.AuthorizationError()

        if len(cleaned_login) < 10:
            raise errors.AuthorizationError()

        cleaned_login = cleaned_login[-10:]

        phone_number = int(cleaned_login)

        password_hash = hash_it(user_info.password)

        user = entities.User(
            phone=phone_number,
            password_hash=password_hash,
            is_staff=user_info.is_staff,
            is_active=user_info.is_active,
            surname=user_info.surname,
            name=user_info.first_name,
            patronymic=user_info.patronymic,
        )
        if user_info.is_staff:
            polygon = self.polygons_repo.get_by_id(user_info.polygon_id)
            if polygon is None:
                raise errors.PolygonIDNotExistError(
                    user_id=user_info.polygon_id
                )

            operator = self.users_repo.get_by_id(user_info.operator_id)
            if operator is None:
                raise errors.UserIDNotExistError(user_id=user_info.operator_id)
            user.staff = Staff(
                role=user_info.role,
                polygon=polygon,
                user=user,
                added_by=operator,
            )

        self.users_repo.add(user)
        self.users_repo.save()

    @join_point
    @validate_with_dto
    def update(self, user_info: UserUpdateInfo):
        user = self.users_repo.get_by_id(user_info.id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=user_info.id)

        polygon = self.polygons_repo.get_by_id(user_info.polygon_id)
        if polygon is None:
            raise errors.PolygonIDNotExistError(user_id=user_info.polygon_id)

        user.is_staff = user_info.is_staff
        user.is_active = user_info.is_active
        if user.staff:
            user.staff.role = user_info.role
            user.staff.polygon = polygon

        if not user.staff and user_info.is_staff:
            operator = self.users_repo.get_by_id(user_info.operator_id)
            if operator is None:
                raise errors.UserIDNotExistError(user_id=user_info.operator_id)

            user.staff = Staff(
                role=user_info.role,
                polygon=polygon,
                user=user,
                added_by=operator,
            )


        self.users_repo.save()

    @join_point
    @validate_arguments
    def update_pass(
        self,
        user_id: int,
        new_pass: str,
    ):
        user = self.users_repo.get_by_id(user_id)
        if user is None:
            raise errors.UserIDNotExistError(user_id=user_id)

        user.password_hash = hash_it(new_pass)

        self.users_repo.save()
