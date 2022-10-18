import json
from typing import Tuple, Union

from falcon import media

from classic.http_api import App

from magnit.adapters.http_api import serializer, controllers
from magnit.application import services


def create_app(
    user: services.User,
    user_group: services.UserGroup,
    contragent: services.Contragent,
    polygon: services.Polygon,
    secondary_route: services.SecondaryRoute,
    vehicle_model: services.VehicleModel,
    vehicle: services.Vehicle,
    permit: services.Permit,
    permit_log: services.PermitLog
) -> App:
    app = App(prefix='/api')

    app.register(controllers.users.Users(service=user))
    app.register(controllers.users.UserGroups(service=user_group))
    app.register(controllers.contragents.Contragents(service=contragent))
    app.register(controllers.polygons.Polygons(service=polygon))
    app.register(controllers.polygons.SecondaryRoutes(service=secondary_route))
    app.register(controllers.vehicles.VehicleModels(service=vehicle_model))
    app.register(controllers.vehicles.Vehicles(service=vehicle))
    app.register(controllers.permits.Permits(service=permit))
    app.register(controllers.permits.PermitsLog(service=permit_log))

    def handler_serialize(obj):
        return json.dumps(serializer.serialize(obj), ensure_ascii=False)

    json_handler = media.JSONHandler(dumps=handler_serialize)

    extra_handlers = {
        'application/json': json_handler,
    }

    app.resp_options.media_handlers.update(extra_handlers)

    return app
