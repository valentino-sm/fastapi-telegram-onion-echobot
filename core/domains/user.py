from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    is_bot: bool
    language_code: str | None
