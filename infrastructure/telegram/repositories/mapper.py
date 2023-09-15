from typing import Any, Mapping, Protocol, TypeVar

T = TypeVar("T", covariant=True)


class MapperRepository(Protocol[T]):
    @classmethod
    def to_domain(cls, object_raw: Mapping[Any, Any]) -> T:
        raise NotImplementedError
