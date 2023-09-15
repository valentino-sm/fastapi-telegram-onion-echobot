from typing import Protocol

from core.domains.message import Message


class MessengerRepository(Protocol):
    @classmethod
    async def send_message(cls, chat_id: int, text: str) -> Message:
        raise NotImplementedError
