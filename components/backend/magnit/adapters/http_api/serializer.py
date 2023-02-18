from dataclasses import asdict, is_dataclass
from datetime import datetime, time, timezone
from enum import Enum, EnumMeta, IntEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel


def serialize(obj: Any):
    """Функция рекурсивно преобразовывает объекты в вид,
    готовый для к сериализации в JSON"""

    if isinstance(obj, (datetime, time)):
        return obj.replace(tzinfo=timezone.utc).isoformat()

    if isinstance(obj, (Enum, IntEnum)):
        return obj.value

    if isinstance(obj, EnumMeta):
        return [serialize(x) for x in obj]

    if isinstance(obj, UUID):
        return obj.hex

    if isinstance(obj, list):
        return [serialize(x) for x in obj]

    if isinstance(obj, dict):
        return {key: serialize(value) for key, value in obj.items()}

    if is_dataclass(obj):
        return serialize(asdict(obj))

    if isinstance(obj, bytes):
        return obj.decode('utf-8')

    if isinstance(obj, BaseModel):
        return serialize(dict(obj))

    return obj
