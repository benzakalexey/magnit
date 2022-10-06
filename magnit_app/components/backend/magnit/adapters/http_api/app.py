import json
from typing import Tuple, Union

from falcon import media

from classic.http_api import App

import magnit.adapters.http_api.controllers.users
from magnit.adapters.http_api import serializer, controllers
from magnit.application import services


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    user: services.User,
    user_group: services.UserGroup,
    contragent: services.Contragent,
    polygon: services.Polygon,
) -> App:
    app = App(prefix='/api')

    app.register(controllers.users.Users(service=user))
    app.register(controllers.users.UserGroups(service=user_group))
    app.register(controllers.contragents.Contragents(service=contragent))
    app.register(controllers.polygons.Polygons(service=polygon))

    def handler_serialize(obj):
        return json.dumps(serializer.serialize(obj), ensure_ascii=False)

    json_handler = media.JSONHandler(dumps=handler_serialize)

    extra_handlers = {
        'application/json': json_handler,
    }

    app.resp_options.media_handlers.update(extra_handlers)

    return app
