import json
from typing import Tuple, Union

import falcon
from falcon import media

from classic.http_api import App

from magnit.adapters.http_api import serializer


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    # add services
) -> App:
    app = App(prefix='/api')

    # app.register() регистрация контроллеров

    def handler_serialize(obj):
        return json.dumps(serializer.serialize(obj), ensure_ascii=False)

    json_handler = media.JSONHandler(dumps=handler_serialize)

    extra_handlers = {
        'application/json': json_handler,
    }

    app.resp_options.media_handlers.update(extra_handlers)

    return app
