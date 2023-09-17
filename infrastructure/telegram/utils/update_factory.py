from typing import Any, Mapping

from infrastructure.telegram.mappers.message import MapperMessage
from infrastructure.telegram.repositories.mapper import MapperRepository
from infrastructure.telegram.utils.exceptions import UnknownMapperException


class UpdateFactory:
    modules: dict[str, MapperRepository[object]] = {
        "message": MapperMessage,
        # "edited_message": MapperEditedMessage,
        # "channel_post": MapperChannelPost,
        # "edited_channel_post": MapperEditedChannelPost,
    }

    @classmethod
    def create(cls, update_type: str, raw_update_obj: Mapping[Any, Any]) -> object:
        if update_type not in cls.modules:
            raise UnknownMapperException(update_type, raw_update_obj)

        return cls.modules[update_type].to_domain(raw_update_obj)
