"""
    Uvicorn Main
"""
from api.main import app


def startup_once():
    from utils.logging import logger
    from utils.settings import settings

    logger.debug(f"Starting server FastAPI {app.version}")

    if settings.is_ngrok_enabled():
        from infrastructure.ngrok import ngrok_setup_url

        settings.tg_webhook_custom_url = ngrok_setup_url()

    import asyncio

    from infrastructure.telegram.client import TelegramClient

    future = TelegramClient.setup_webhook(settings.get_tg_webhook_url())
    asyncio.run(future)


@app.on_event("startup")
def startup_for_every_worker():
    from utils.dependencies import dependencies_setup

    dependencies_setup()


if __name__ == "__main__":
    startup_once()

    import uvicorn

    from utils.settings import settings

    uvicorn.run(  # type: ignore
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
        workers=4,
    )
