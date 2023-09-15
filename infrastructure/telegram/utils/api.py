from typing import Any

from infrastructure.http import request
from infrastructure.telegram.utils.exceptions import EmptyMessageException

from utils.settings import settings


class TelegramAPI:
    url = f"https://api.telegram.org/bot{settings.tg_token}"

    @classmethod
    async def set_webhook(
        cls, url: str, allowed_updates: list[str] | None = None
    ) -> dict[Any, Any]:
        """
        Telegram specifies an empty list to receive all update types except chat_member
        """
        if not allowed_updates:
            allowed_updates = [
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
                "inline_query",
                "chosen_inline_result",
                "callback_query",
                "shipping_query",
                "pre_checkout_query",
                "poll",
                "poll_answer",
                "my_chat_member",
                "chat_member",
                "chat_join_request",
            ]
        payload = {
            "url": f"{url}",
            "allowed_updates": allowed_updates,
        }
        return await request("POST", url=f"{cls.url}/setWebhook", json=payload)

    @classmethod
    async def send_message(cls, chat_id: int, text: str) -> dict[Any, Any]:
        if not text:
            raise EmptyMessageException("Text cannot be empty")
        payload = {"chat_id": chat_id, "text": text}
        return await request("POST", url=f"{cls.url}/sendMessage", json=payload)
