# pyright: basic

import asyncio
import unittest
from os.path import join
from sys import path
from typing import Any, AsyncGenerator, Coroutine

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pyrogram import types
from pyrogram.client import Client


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=join(path[0], ".env"), env_file_encoding="utf-8"
    )

    api_id: str = Field(alias="test_api_id", default="")
    api_hash: str = Field(alias="test_api_hash", default="")


settings = Settings()


class ConversationTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        import os
        import sys

        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from utils.settings import settings

        self.bot_id = settings.tg_token.split(":")[0]

    def tearDown(self):
        pass

    async def test_conversation(self):
        async with Client("my_account", settings.api_id, settings.api_hash) as app:
            r: types.Message = await app.send_message(self.bot_id, "ConversationTest")
            self.assertIsInstance(r, types.Message)
            await asyncio.sleep(3)

            history: Coroutine[
                Any,
                Any,
                AsyncGenerator[types.Message, None] | None,
            ] = app.get_chat_history(self.bot_id, limit=1)
            self.assertIsInstance(history, AsyncGenerator)
            assert isinstance(history, AsyncGenerator)

            async for message in history:
                self.assertIsInstance(message, types.Message)
                self.assertEqual(
                    message.from_user.id,
                    int(self.bot_id),
                    "There is no answer from bot",
                )


if __name__ == "__main__":
    unittest.main(warnings="ignore")
