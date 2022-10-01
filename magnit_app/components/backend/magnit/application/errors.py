from classic.app.errors import AppError


class UserGroupNameIsNoneError(AppError):
    msg_template = 'Имя Группы пользователей не может быть пустым.'
    code = 'magnit.users.user_group_name_is_none_error'

class ContragentNameIsNoneError(AppError):
    msg_template = 'Название контрагента не может быть пустым.'
    code = 'magnit.contragentss.contragent_name_is_none_error'
