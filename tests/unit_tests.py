import os
import sys
import unittest
from unittest import mock

from test_settings import TestSettingsCustom  # noqa: F401 # pyright: ignore
from test_settings import TestSettingsNgrok  # noqa: F401 # pyright: ignore
from test_settings import TestSettingsStandard  # noqa: F401 # pyright: ignore

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestHTTP(unittest.IsolatedAsyncioTestCase):
    async def test_request(self):
        from infrastructure.http import request

        mock_logger = mock.patch("utils.logging.Logger._log")
        mock_logger.start()

        with mock.patch(
            "infrastructure.http.AsyncClient", new_callable=mock.MagicMock
        ) as magicmock:
            magicmock.return_value.__aenter__.return_value.request.return_value = (
                mock.MagicMock(json=lambda: {"ok": True})
            )
            result = await request("GET", "https://www.google.com/")
            self.assertEqual(result, {"ok": True})

        mock_logger.stop()


class TestMapping(unittest.TestCase):
    def test_mapper(self):
        from mock_data import tg_message

        from core.domains.message import Message
        from infrastructure.telegram.utils.update_factory import UpdateFactory

        # SuccessMapping
        message = UpdateFactory.create("message", tg_message)
        self.assertIsInstance(message, Message)
        assert isinstance(message, Message)  # pyright hack
        self.assertEqual(message.id, 1)

        # UnknownMapper
        from infrastructure.telegram.utils.exceptions import \
            UnknownMapperException

        self.assertRaises(
            UnknownMapperException, UpdateFactory.create, "message_bug", tg_message
        )

        # UnsuccessMapper
        from infrastructure.telegram.utils.exceptions import \
            UnsuccessMapperException

        tg_message["message_id"] = "error_text"
        self.assertRaises(
            UnsuccessMapperException, UpdateFactory.create, "message", tg_message
        )


class TestRouterProcessUpdates(unittest.IsolatedAsyncioTestCase):
    async def test_process_update(self):
        from api.telegram import process_updates

        with mock.patch("utils.logging.Logger._log") as logger_mock:
            # Unsucess
            u = 1
            await process_updates(u)
            logger_mock.assert_called_with(
                30,
                f"api.telegram: InvalidUpdateTypeException: ({type(u)}, {u})",
            )
            u = "test"
            await process_updates(u)
            logger_mock.assert_called_with(
                30,
                f"api.telegram: InvalidUpdateTypeException: ({type(u)}, '{u}')",
            )

            # Success
            with mock.patch(
                "api.telegram.TelegramController.process_update"
            ) as magicmock:
                u = {"sometest": 42}
                await process_updates(u)
                magicmock.assert_called_with(u)
                magicmock.reset_mock()

                u = [{"sometest": 43}, "bug", {"sometest": 44}]
                await process_updates(u)
                magicmock.assert_called_with(u[-1])
                self.assertEqual(magicmock.call_count, 2)


class TestControllerProcessUpdates(unittest.IsolatedAsyncioTestCase):
    async def test_process_update(self):
        self.logger_mock = mock.patch("utils.logging.Logger._log")
        self.logger_mock.start()
        from infrastructure.telegram.controller import TelegramController
        from infrastructure.telegram.utils.exceptions import \
            InvalidUpdateValueException

        update = {"sometest": 42}
        with self.assertRaises(InvalidUpdateValueException):
            await TelegramController.process_update(update)

        update = {"update_id": 42}
        with self.assertRaises(InvalidUpdateValueException):
            await TelegramController.process_update(update)

        from infrastructure.telegram.utils.exceptions import \
            UnknownMapperException

        update = {"update_id": 42, "update_type": "test"}
        with self.assertRaises(UnknownMapperException):
            await TelegramController.process_update(update)

        from infrastructure.telegram.utils.exceptions import \
            UnsuccessMapperException

        update = {"update_id": 42, "message": "test"}
        with self.assertRaises(UnsuccessMapperException):
            await TelegramController.process_update(update)

        # Success
        from mock_data import tg_message

        from infrastructure.telegram.utils.update_factory import UpdateFactory

        TelegramController.conversation = mock.AsyncMock()
        process_event = mock.AsyncMock()
        TelegramController.conversation.process_event = process_event

        update = {"update_id": 42, "message": tg_message}
        await TelegramController.process_update(update)
        process_event.assert_called_with(UpdateFactory.create("message", tg_message))

        self.logger_mock.stop()


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.logger_mock = mock.patch("utils.logging.Logger._log")
        self.logger_mock.start()

        from fastapi.testclient import TestClient

        from api.main import app

        self.client = TestClient(app)

    def tearDown(self):
        self.logger_mock.stop()

    def test_tg_token_router(self):
        from utils.settings import settings

        prefix = settings.tg_prefix
        token = settings.tg_token

        from fastapi import status

        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f"{prefix}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.get(f"{prefix}/bad-token-{token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(f"{prefix}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(f"{prefix}/bad-token-{token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Good Token but empty
        response = self.client.get(f"{prefix}/{token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.post(f"{prefix}/{token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # JSONDecodeError
        response = self.client.post(f"{prefix}/{token}", content="bug")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(f"{prefix}/{token}", json={"text": "test"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response = self.client.post(f"{prefix}/{token}", json={"update_id": "test"})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response = self.client.post(f"{prefix}/{token}", json={"update_id": 1})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


if __name__ == "__main__":
    import logging

    logging.getLogger("asyncio").setLevel(logging.ERROR)
    unittest.main()
