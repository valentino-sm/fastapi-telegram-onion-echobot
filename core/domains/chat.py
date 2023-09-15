from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chat:
    id: int
    type: str
    first_name: str | None
    last_name: str | None
    username: str | None
