from typing import Callable, ParamSpec, TypeVar

from pydantic import ValidationError

from infrastructure.telegram.utils.exceptions import UnsuccessMapperException

T = TypeVar("T")
P = ParamSpec("P")


def exception_wrapper(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except (TypeError, KeyError, AttributeError, ValidationError) as e:
            raise UnsuccessMapperException(e, args, kwargs) from e

    return wrapper
