import json
from classic.http_api import App
from falcon import media, CORSMiddleware

from magnit.adapters.http_api import serializer, controllers
from magnit.application import services


def create_app(
    allow_all_origins,
    auth_service: services.Auth,
    contragent: services.Contragent,
    doc: services.Doc,
    doc_log: services.DocLog,
    permit: services.Permit,
    polygon: services.Polygon,
    secondary_route: services.SecondaryRoute,
    user: services.User,
    vehicle: services.Vehicle,
    vehicle_model: services.VehicleModel,
    visit: services.Visit,
) -> App:
    # cors = CORS(
    #     allow_all_origins=allow_all_origins,
    #     # allow_origins_list=["http://0.0.0.0:8080/",],
    #     # allow_origins_regex=None,
    #     # allow_credentials_all_origins=True,
    #     allow_credentials_origins_list=["http://0.0.0.0:8080/", "http://127.0.0.1/",  "http://127.0.0.1:8080/", ],
    #     # allow_credentials_origins_regex=None,
    #     allow_all_headers=True,
    #     # allow_headers_list=[],
    #     # allow_headers_regex=None,
    #     # expose_headers_list=[],
    #     allow_all_methods=True,
    #     # allow_methods_list=whitelisted_methods
    # )
    app = App(
        prefix='/api',
        cors_enable=True,
        # middleware=CORSMiddleware(
        #     allow_origins="*",
        #     # [
        #     #     "http://0.0.0.0:8080/",
        #     #     "http://127.0.0.1/",
        #     #     "http://127.0.0.1:8080/",
        #     # ],
        #     allow_credentials='*',
        # )
    )

    app.register(controllers.Auth(service=auth_service))
    app.register(controllers.Contragents(service=contragent))
    app.register(controllers.DocLogs(service=doc_log))
    app.register(controllers.Docs(service=doc))
    app.register(controllers.Permits(service=permit))
    app.register(controllers.Polygons(service=polygon))
    app.register(controllers.SecondaryRoutes(service=secondary_route))
    app.register(controllers.Users(service=user))
    app.register(controllers.VehicleModels(service=vehicle_model))
    app.register(controllers.Vehicles(service=vehicle))
    app.register(controllers.Visits(service=visit))

    def handler_serialize(obj):
        return json.dumps(serializer.serialize(obj), ensure_ascii=False)

    json_handler = media.JSONHandler(dumps=handler_serialize)

    extra_handlers = {
        'application/json': json_handler,
    }

    app.resp_options.media_handlers.update(extra_handlers)

    return app
