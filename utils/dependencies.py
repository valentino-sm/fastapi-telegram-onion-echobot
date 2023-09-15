from core.services.conversation import ConversationService
from infrastructure.telegram.client import TelegramClient
from infrastructure.telegram.controller import TelegramController


def dependencies_setup() -> None:
    TelegramController.conversation = ConversationService(TelegramClient)
