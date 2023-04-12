import json
from classic.http_api import App
from falcon import media, CORSMiddleware

from magnit.adapters.http_api import serializer, controllers
from magnit.application import services


def create_app(
    allow_all_origins,
    auth_service: services.Auth,
    contragent: services.Partner,
    permit: services.Permit,
    polygon: services.Polygon,
    user: services.User,
    driver: services.Driver,
    truck: services.Truck,
    # truck_model: services.TruckModel,
    visit: services.Visit,
) -> App:
    app = App(
        prefix='/api',
        cors_enable=True,
        middleware=CORSMiddleware(
            allow_origins=allow_all_origins,
            allow_credentials='*',
        )
    )
    app.register(controllers.Auth(service=auth_service))
    app.register(controllers.Partners(service=contragent))
    app.register(controllers.Permits(service=permit))
    app.register(controllers.Polygons(service=polygon))
    # app.register(controllers.SecondaryRoutes(service=secondary_route))
    app.register(controllers.Users(service=user))
    app.register(controllers.Drivers(service=driver))
    # app.register(controllers.truckModels(service=truck_model))
    app.register(controllers.Trucks(service=truck))
    app.register(controllers.Visits(service=visit))

    def handler_serialize(obj):
        return json.dumps(serializer.serialize(obj), ensure_ascii=False)

    json_handler = media.JSONHandler(dumps=handler_serialize)

    extra_handlers = {
        'application/json': json_handler,
    }

    app.resp_options.media_handlers.update(extra_handlers)

    return app
