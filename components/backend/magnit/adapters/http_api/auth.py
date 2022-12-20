import functools

from magnit.application import errors
from magnit.application.services.auth import Token, Authenticator


def authorize():
    def decorator(func):
        resource_name = func.__qualname__

        @functools.wraps(func)
        def wrapper(controller, request, response):
            client = request.context.client

            # if not spec.is_satisfied_by(client):
            #     raise errors.PermissionDenied(resource_name=resource_name)

            result = func(controller, request, response)
            return result

        return wrapper

    return decorator


def authenticate(func):
    @functools.wraps(func)
    def wrapper(controller, request, response):
        if request.auth is None:
            raise errors.AuthenticationError()

        try:
            _, auth_token = request.auth.strip().split()
        except TypeError:
            raise errors.AuthenticationError()

        try:
            Token.check(auth_token, Authenticator().secret)
        except (errors.TokenDecodeError, errors.TokenExpiredError):
            raise errors.AuthenticationError()

        return func(controller, request, response)

    return wrapper
