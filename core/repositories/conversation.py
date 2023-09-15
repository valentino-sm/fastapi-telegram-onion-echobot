from functools import singledispatchmethod
from typing import Protocol


class ConversationRepository(Protocol):
    @singledispatchmethod
    async def process_event(self, object: object) -> None:
        raise NotImplementedError
