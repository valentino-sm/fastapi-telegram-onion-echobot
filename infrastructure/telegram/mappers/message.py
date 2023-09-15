from typing import Any, Mapping

from pydantic import TypeAdapter

from core.domains.message import Message
from infrastructure.telegram.repositories.mapper import MapperRepository


class Mapper(MapperRepository[Message]):
    adapter_message = TypeAdapter(Message)

    @classmethod
    def to_domain(cls, object_raw: Mapping[Any, Any]) -> Message:
        message = object_raw
        result = {
            "id": message["message_id"],
            "text": message["text"],
            "date": message["date"],
            "user": {
                "id": message["from"]["id"],
                "first_name": message["from"]["first_name"],
                "last_name": message["from"].get("last_name"),
                "username": message["from"].get("username"),
                "is_bot": message["from"]["is_bot"],
                "language_code": message["from"].get("language_code"),
            },
            "chat": {
                "id": message["chat"]["id"],
                "type": message["chat"]["type"],
                "first_name": message["chat"].get("first_name"),
                "last_name": message["chat"].get("last_name"),
                "username": message["chat"].get("username"),
            },
            "reply_to_id": message.get("reply_to_message", {}).get("message_id"),
        }
        return cls.adapter_message.validate_python(result)
