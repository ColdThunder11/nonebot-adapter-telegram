from nonebot import adapters
from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """
    telegram配置类

    :配置项:

      - ``webhook_host`` / ``telegram_webhook_host``: webhook的host
      - ``bot_token`` / ``telegram_bot_token``: bot_token
    """
    webhook_host: Optional[str] = Field(default=None, alias="telegram_webhook_host")
    bot_token: Optional[str] = Field(default=None, alias="telegram_bot_token")
    telegram_adapter_debug: Optional[bool] = Field(default=False, alias="telegram__adapter_debug")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
