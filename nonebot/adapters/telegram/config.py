from nonebot import adapters
from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """
    telegram配置类

    :配置项:

      - ``webhook_host`` / ``telegram_webhook_host``: webhook的host
      - ``bot_token`` / ``telegram_bot_token``: bot_token
      - ``telegram_command_only`` / ``telegram_command_only``: 不处理非command的消息 #还无效
      - ``telegram_bot_server_addr`` / ``telegram_bot_server_addr``: telegram bot api服务器地址，默认为官方
    """
    webhook_addr: Optional[str] = Field(default=None, alias="telegram_webhook_host")
    bot_token: Optional[str] = Field(default=None, alias="telegram_bot_token")
    telegram_adapter_debug: Optional[bool] = Field(default=False, alias="telegram_adapter_debug")
    telegram_command_only: Optional[bool] = Field(default=False, alias="telegram_command_only")
    telegram_bot_api_server_addr: Optional[str] = Field(default="https://api.telegram.org", alias="telegram_bot_server_addr")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
