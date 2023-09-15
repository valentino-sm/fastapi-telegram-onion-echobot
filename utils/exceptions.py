import inspect
from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

from utils.logging import logger


class QuietException(Exception):
    pass


T = TypeVar("T")
P = ParamSpec("P")


def exceptions_log(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T | None]]:
    @wraps(func)
    async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> T | None:
        try:
            return await func(*args, **kwargs)
        except QuietException as e:
            frm = inspect.trace()[-1]
            module = inspect.getmodule(frm[0])
            module_name = module.__name__ if module else "UnknownModule"
            log = f"{module_name}: {type(e).__name__}: {e}"
            logger.warning(log)
        except Exception as e:
            log = f"{type(e).__name__}: {e}"
            logger.error(log)
            raise

    return async_wrapper
