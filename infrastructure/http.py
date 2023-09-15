from typing import Any

from httpx import AsyncClient
from tenacity import (
    RetryCallState,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential,
    wait_random,
)

from utils.exceptions import QuietException
from utils.logging import logger


class RetryException(QuietException):
    pass


def is_not_valid(value: Any) -> bool:
    return not isinstance(value, dict) or not value


def error_callback(retry_state: RetryCallState) -> None:
    raise RetryException(retry_state, retry_state.args, retry_state.kwargs)


@retry(
    retry=retry_if_result(is_not_valid) | retry_if_exception_type(Exception),
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=1, min=1, max=10) + wait_random(min=0.1, max=0.5),
    retry_error_callback=error_callback,
)
async def request(*args: Any, **kwargs: Any) -> dict[Any, Any]:
    async with AsyncClient() as client:
        response = await client.request(*args, **kwargs)
    response.raise_for_status()
    result = response.json()
    logger.debug(f"Response: {result}")
    return result
