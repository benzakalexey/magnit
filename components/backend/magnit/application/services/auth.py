from classic.components import component

from magnit.application import interfaces


@component
class AAA:
    """Autenification, Authorization, Audit
    """

    # tokens_blacklist: interfaces.TokensBlacklistRepo
    users: interfaces.UserRepo


