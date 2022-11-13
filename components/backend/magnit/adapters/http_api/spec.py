from typing import List, Tuple

from falcon import App

from evraz.classic.http_api import HTTP_ERROR_STATUS_CODE
from evraz.classic.http_api.error_models import AllPossibleErrors
from evraz.spectree import SpecTree
from evraz.spectree.models import Server

spectree = SpecTree(
    'falcon',
    mode='strict',
    annotations=True,
    version='v1.0',
    validation_error_status=HTTP_ERROR_STATUS_CODE,
    validation_error_model=AllPossibleErrors,
)


def setup_spectree(
    app: App,
    title: str,
    path: str,
    filename: str,
    servers: List[Tuple[str, str]],
):
    servers = [
        Server(url=url, description=description) for url, description in servers
    ]

    spectree.update_config(
        title=title,
        path=path,
        filename=filename,
        servers=servers,
    )

    spectree.register(app)
