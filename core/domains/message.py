from dataclasses import dataclass
from datetime import datetime

from core.domains.chat import Chat
from core.domains.user import User


@dataclass(frozen=True, slots=True)
class Message:
    id: int
    user: User
    chat: Chat
    text: str
    date: datetime
    reply_to_id: int | None
