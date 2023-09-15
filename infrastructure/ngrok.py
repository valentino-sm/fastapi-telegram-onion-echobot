# pyright: basic

import logging

from pyngrok import ngrok

from utils.logging import logger
from utils.settings import settings


def ngrok_setup_url() -> str:
    logging.getLogger("pyngrok").setLevel(logging.ERROR)
    tunnel = ngrok.connect(settings.port, bind_tls=True)
    logger.debug(f"Public URL: {tunnel.public_url}")
    return tunnel.public_url
