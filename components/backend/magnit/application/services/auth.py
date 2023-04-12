import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta

from classic.app import DTO, validate_with_dto
from classic.components import component
from jwt import AbstractJWKBase, JWT, jwk_from_dict
from jwt.exceptions import JWTException

from magnit.application import interfaces, errors
from magnit.application.services.join_point import join_point

APP_ISSUER = 'https://magnit.tw1.ru'
TOKEN_LIVE_HOURS = 1200


def hash_it(i: str):
    return hashlib.sha512(i.encode('utf-8')).digest()


class AuthInfo(DTO):
    login: str
    password: str


@component
class Auth:
    users_repo: interfaces.UserRepo

    @join_point
    @validate_with_dto
    def login(self, auth_info: AuthInfo):

        cleaned_login = re.sub('[^0-9]+', '', auth_info.login)

        if not cleaned_login.isalnum():
            raise errors.AuthorizationError()

        if len(cleaned_login) < 10:
            raise errors.AuthorizationError()

        cleaned_login = cleaned_login[-10:]
        phone_number = int(cleaned_login)

        user = self.users_repo.get_by_phone(phone_number)
        if user is None:
            raise errors.AuthorizationError()

        password_hash = hash_it(auth_info.password)
        if password_hash != user.password_hash:
            raise errors.AuthorizationError()

        token = Token(user.id).encode(secret=Authenticator().secret)

        return user, token


@dataclass
class Token:
    uid: int
    exp: int = field(default_factory=lambda: int(
        (datetime.utcnow() + timedelta(hours=TOKEN_LIVE_HOURS)).timestamp()
    ))
    iat: int = field(default_factory=lambda: int(datetime.utcnow().timestamp()))
    iss: str = APP_ISSUER

    def encode(self, secret: AbstractJWKBase):
        return JWT().encode(asdict(self), secret)

    @classmethod
    def check(
        cls,
        payload: str,
        secret: AbstractJWKBase,
    ) -> 'Token':
        data = cls._decode(payload, secret)

        try:
            exp = data['exp']
            iat = data['iat']
            uid = data['uid']
            iss = data['iss']
        except KeyError:
            raise errors.TokenDecodeError()

        if iss != APP_ISSUER:
            raise errors.TokenDecodeError()

        if not isinstance(exp, int):
            raise errors.TokenDecodeError()

        expired_at = datetime.fromtimestamp(exp)
        iat_d = datetime.fromtimestamp(iat)
        if expired_at <= datetime.utcnow():
            raise errors.TokenExpiredError()

        if not isinstance(uid, int):
            raise errors.TokenExpiredError()

        if (int((datetime.fromtimestamp(exp) -
                 timedelta(hours=TOKEN_LIVE_HOURS)).timestamp()) != iat):
            ...  # raise errors.TokenExpiredError() TODO TURN ON BEFORE DEPLOY

        try:
            token = cls(
                exp=exp,
                iat=iat,
                uid=uid,
                iss=iss,
            )
        except TypeError:
            raise errors.TokenDecodeError()

        return token

    @classmethod
    def _decode(cls, payload: str, secret: AbstractJWKBase):
        try:
            decoded = JWT().decode(payload, secret, do_time_check=False)
        except JWTException:
            raise errors.TokenDecodeError()

        return decoded


@dataclass
class Authenticator:
    key: str = ''
    secret: AbstractJWKBase = field(init=False)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __post_init__(self):
        self.secret = jwk_from_dict({'kty': 'oct', 'k': self.key})
