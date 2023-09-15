from os.path import join
from sys import path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=join(path[0], ".env"), env_file_encoding="utf-8"
    )

    debug: bool = False
    host: str = Field(default_factory=str)
    port: int = 8000

    tg_token: str = Field(default_factory=str)
    tg_prefix: str = "/tg"
    tg_webhook_custom_url: str = ""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.host = self.host.rstrip("/")
        self.tg_prefix = "/" + self.tg_prefix.strip("/")
        self.tg_webhook_custom_url = self.tg_webhook_custom_url.rstrip("/")

    def get_tg_webhook_url(self):
        if self.tg_webhook_custom_url:
            result = self.tg_webhook_custom_url
        else:
            result = f"{self.host}:{self.port}"

        if "://" not in result:
            result = f"https://{result}"
        return f"{result}{self.tg_prefix}/{self.tg_token}"

    def is_ngrok_enabled(self) -> bool:
        return self.tg_webhook_custom_url.startswith("ngrok")


settings = Settings()
