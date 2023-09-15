from core.domains.message import Message
from core.repositories.messenger import MessengerRepository
from infrastructure.telegram.utils.api import TelegramAPI
from infrastructure.telegram.utils.exceptions import (
    FailedMessageResponseException, WebhookException)
from infrastructure.telegram.utils.mapper import Mapper


class TelegramClient(MessengerRepository):
    @classmethod
    async def setup_webhook(cls, url: str) -> None:
        response = await TelegramAPI.set_webhook(url=url)
        if not response.get("result"):
            raise WebhookException("Failed to setup webhook")

    @classmethod
    async def send_message(cls, chat_id: int, text: str) -> Message:
        response = await TelegramAPI.send_message(chat_id=chat_id, text=text)
        match response:
            case {"ok": True, "result": raw_message}:
                return Mapper[Message].to_domain("message", raw_message)
            case _:
                raise FailedMessageResponseException(response)
