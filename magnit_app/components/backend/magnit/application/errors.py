from classic.app.errors import AppError


class UserFirstNameIsNoneError(AppError):
    msg_template = 'Имя Пользователя не может быть пустым.'
    code = 'magnit.users.user_first_name_is_none_error'


class UserLastNameIsNoneError(AppError):
    msg_template = 'Фамилия Пользователя не может быть пустой.'
    code = 'magnit.users.user_last_name_is_none_error'


class UserIDNotExistError(AppError):
    msg_template = 'Пользователь с id = {user_id} не найден'
    code = 'magnit.users.user_id_not_exist_error'


class ContragentNameIsNoneError(AppError):
    msg_template = 'Название контрагента не может быть пустым.'
    code = 'magnit.contragents.contragent_name_is_none_error'


class ContragentIDNotExistError(AppError):
    msg_template = 'Контрагент с id = {contragent_id} не найден'
    code = 'magnit.contragents.contragent_id_not_exist_error'


class PolygonNameIsNoneError(AppError):
    msg_template = 'Название полигона не может быть пустым.'
    code = 'magnit.polygons.polygon_name_is_none_error'


class PolygonIDNotExistError(AppError):
    msg_template = 'Полигон с id = {polygon_id} не найден'
    code = 'magnit.polygons.polygon_id_not_exist_error'


class SecondaryRouteIDNotExistError(AppError):
    msg_template = 'Запись с id = {secondary_route_id} не найдена'
    code = 'magnit.polygons.secondary_route_id_not_exist_error'


class VehicleModelNameIsNoneError(AppError):
    msg_template = 'Название модели автомобиля не может быть пустым.'
    code = 'magnit.vehicles.vehicle_model_name_is_none_error'


class VehicleModelIDNotExistError(AppError):
    msg_template = 'Модель автомобиля с id = {vehicle_model_id} не найдена'
    code = 'magnit.vehicles.vehicle_model_id_not_exist_error'


class VehicleNameIsNoneError(AppError):
    msg_template = 'Название автомобиля не может быть пустым.'
    code = 'magnit.vehicles.vehicle_name_is_none_error'


class VehicleIDNotExistError(AppError):
    msg_template = 'Автомобиль с id = {vehicle_id} не найден'
    code = 'magnit.vehicles.vehicle_id_not_exist_error'


class PermitIDNotExistError(AppError):
    msg_template = 'Пропуск с id = {permit_id} не найден'
    code = 'magnit.permits.permit_id_not_exist_error'


class PermitLogIDNotExistError(AppError):
    msg_template = 'Запись в журнале пропусков с id = {permit_log_id} не найдена'
    code = 'magnit.permits.permit_log_id_not_exist_error'


class VisitIDNotExistError(AppError):
    msg_template = 'Визит с id = {visit_id} не найден'
    code = 'magnit.visits.visit_id_not_exist_error'


class DocLogIDNotExistError(AppError):
    msg_template = 'Запись с id = {doc_log_id} не найдена'
    code = 'magnit.doclogs.doc_log_id_not_exist_error'
