import asyncio
import json
import random
from typing import Any, Mapping, Sequence

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from infrastructure.telegram.controller import TelegramController
from infrastructure.telegram.utils.exceptions import InvalidUpdateTypeException

from utils.exceptions import exceptions_log
from utils.settings import settings

router = APIRouter(prefix=settings.tg_prefix, include_in_schema=False)


async def verify_token(token: str) -> None:
    if token == settings.tg_token:
        return
    await asyncio.sleep(random.random() * 0.05)  # Paranoic protection from bruteforce
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@exceptions_log
async def process_update(raw_update: Mapping[Any, Any] | Any) -> None:
    if not isinstance(raw_update, dict):
        raise InvalidUpdateTypeException(type(raw_update), raw_update)
    await TelegramController.process_update(raw_update)


async def process_updates(raw_update: Sequence[Any] | Any) -> None:
    if isinstance(raw_update, list):
        for update in raw_update:
            await process_update(update)
    else:
        await process_update(raw_update)


@router.post("/{token}", dependencies=[Depends(verify_token)], include_in_schema=False)
async def post_webhook(request: Request, background_tasks: BackgroundTasks) -> Response:
    body = await request.body()
    try:
        update = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    background_tasks.add_task(process_updates, update)
    return Response(status_code=status.HTTP_202_ACCEPTED)


# Faking GET Request to avoid 405 Method Not Allowed
@router.get("/{any_token}", include_in_schema=False)
async def get() -> Response:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
