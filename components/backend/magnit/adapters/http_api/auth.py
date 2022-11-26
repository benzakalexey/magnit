from classic.http_auth import Authenticator, Group, Permission
from classic.http_auth import strategies as auth_strategies

full_control = Permission('full_control')
read_only = Permission('read_only')

groups = (
    Group('admins', permissions=[full_control]),
    Group('managers', permissions=[read_only]),
    Group('guests'),
)

auth_strategy = auth_strategies.JWT(secret_key='123')

auth_dummy_strategy = auth_strategies.Dummy(
    login='login',
    name='name',
    groups=groups,
    email='email'
)

authenticator = Authenticator(app_groups=groups)

is_dev = True
if is_dev:
    authenticator.set_strategies(auth_dummy_strategy)
else:
    authenticator.set_strategies(auth_strategy)
