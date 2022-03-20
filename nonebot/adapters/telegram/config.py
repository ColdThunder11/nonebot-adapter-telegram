from nonebot import adapters
from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """
    telegram配置类

    :配置项:

      - ``webhook_host`` / ``telegram_webhook_host``: webhook的host
      - ``bot_token`` / ``telegram_bot_token``: bot_token
      - ``telegram_command_only`` / ``telegram_command_only``: 不处理非command的消息 #还无效先占着
      - ``telegram_bot_server_addr`` / ``telegram_bot_server_addr``: telegram bot api服务器地址，默认为官方
      - ``telegram_bot_api_proxy`` / ``telegram_bot_api_proxy``: 代理服务器地址，需满足httpx代理的格式，默认为None
      - ``telegram_polling_interval`` / ``telegram_polling_interval``: (仅HTTP轮训模式)HTTP轮训间隔，默认为0，即启用长轮训
      - ``telegram_long_polling_timeout`` / ``telegram_long_polling_timeout``: (仅HTTP轮训模式)HTTP长轮训超时时间，默认为20秒
    """
    webhook_addr: Optional[str] = Field(default=None, alias="telegram_webhook_host")
    bot_token: Optional[str] = Field(default=None, alias="telegram_bot_token")
    telegram_adapter_debug: Optional[bool] = Field(default=False, alias="telegram_adapter_debug")
    telegram_command_only: Optional[bool] = Field(default=False, alias="telegram_command_only")
    telegram_bot_api_server_addr: Optional[str] = Field(default="https://api.telegram.org", alias="telegram_bot_server_addr")
    telegram_bot_api_proxy: Optional[str] = Field(default=None, alias="telegram_bot_api_proxy")
    telegram_polling_interval: Optional[int] = Field(default=0, alias="telegram_polling_interval")
    telegram_long_polling_timeout: Optional[int] = Field(default=20, alias="telegram_long_polling_timeout")
    #telegram_use_webhook:Optional[bool] = Field(default=False, alias="telegram_adapter_debug")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
