from typing import Any, Mapping

from core.repositories.conversation import ConversationRepository
from infrastructure.telegram.utils.exceptions import \
    InvalidUpdateValueException
from infrastructure.telegram.utils.update_factory import UpdateFactory
from utils.logging import logger

UnpackedUpdate = tuple[int, str, Mapping[Any, Any]]


class TelegramController:
    conversation: ConversationRepository

    @classmethod
    async def process_update(cls, update: Mapping[Any, Any]) -> None:
        """
        At most one of the optional parameters can be present in any given update.
        https://core.telegram.org/bots/api#update
        """
        update_id, update_type, raw_update_obj = cls._unpack_update(update)
        logger.debug(f"update_id: {update_id} - {update_type}")
        update_obj = UpdateFactory.create(update_type, raw_update_obj)
        await cls.conversation.process_event(update_obj)

    @staticmethod
    def _unpack_update(update: Mapping[Any, Any]) -> UnpackedUpdate:
        try:
            update_id = int(update["update_id"])
            update_type, update_obj = next(
                (k, v) for k, v in update.items() if k != "update_id"
            )
        except (KeyError, ValueError, StopIteration):
            raise InvalidUpdateValueException(update)
        return (update_id, update_type, update_obj)
