from functools import singledispatchmethod

from core.domains.message import Message
from core.repositories.conversation import ConversationRepository
from core.repositories.messenger import MessengerRepository
from core.services.exceptions import UnknownObjectException

from utils.logging import logger


class ConversationService(ConversationRepository):
    Messenger: type[MessengerRepository]

    def __init__(self, Messenger: type[MessengerRepository]):
        self.Messenger = Messenger

    @singledispatchmethod
    async def process_event(self, object: object) -> None:
        raise UnknownObjectException(object)

    @process_event.register
    async def _(self, message: Message) -> None:
        logger.debug(message)
        await self.Messenger.send_message(message.chat.id, message.text)
