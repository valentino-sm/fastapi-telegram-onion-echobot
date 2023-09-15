from utils.exceptions import QuietException


class UserException(QuietException):
    """Base user exception."""


class UnknownObjectException(UserException):
    """Context from Function conversation.py:process_event"""
