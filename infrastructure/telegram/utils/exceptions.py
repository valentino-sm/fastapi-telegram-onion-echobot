from utils.exceptions import QuietException


class TelegramException(QuietException):
    """Base class for exceptions in this module."""


class InvalidUpdateTypeException(TelegramException):
    """Context from Function api/telegram.py:process_update"""


class InvalidUpdateValueException(TelegramException):
    """Context from Function controller.py:_unpack_update"""


class UnknownMapperException(TelegramException):
    """Context from Function utils/update_factory.py:create"""


class UnsuccessMapperException(TelegramException):
    """Context from Function mappers/exception_wrapper.py:exception_wrapper"""


class WebhookException(TelegramException):
    """Context from Function client.py:setup_webhook"""


class EmptyMessageException(TelegramException):
    """Context from Function utils/api.py:send_message"""


class FailedMessageResponseException(TelegramException):
    """Context from Function client.py:send_message"""
