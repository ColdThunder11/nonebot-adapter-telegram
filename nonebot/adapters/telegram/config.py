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
      - ``telegram_mount_media`` / ``telegram_mount_media``: 在fastapi上挂载本地媒体下载api，开启后可以实时获取图片的本地下载链接
      - ``telegram_media_public_addr`` / ``telegram_media_public_addr``: 媒体下载链接使用公开地址而不是私有地址使插件可以像ob11那样来处理图片，注意潜在的被刷流量风险(x exapmle:https://example.com
      - ``telegram_redis_db`` / ``telegram_redis_db``: 使用redis的db，默认为2以防止和现有应用冲突 
    """
    webhook_addr: Optional[str] = Field(default=None, alias="telegram_webhook_host")
    bot_token: Optional[str] = Field(default=None, alias="telegram_bot_token")
    telegram_adapter_debug: Optional[bool] = Field(default=False, alias="telegram_adapter_debug")
    telegram_command_only: Optional[bool] = Field(default=False, alias="telegram_command_only")
    telegram_bot_api_server_addr: Optional[str] = Field(default="https://api.telegram.org", alias="telegram_bot_server_addr")
    telegram_bot_api_proxy: Optional[str] = Field(default=None, alias="telegram_bot_api_proxy")
    telegram_polling_interval: Optional[int] = Field(default=0, alias="telegram_polling_interval")
    telegram_long_polling_timeout: Optional[int] = Field(default=20, alias="telegram_long_polling_timeout")
    telegram_mount_media: Optional[bool] = Field(default=True, alias="telegram_mount_media")
    telegram_media_public_addr: Optional[str] = Field(default=None, alias="telegram_media_public_addr")
    telegram_redis_db: Optional[int] = Field(default=2, alias="telegram_redis_db")
    #telegram_use_webhook:Optional[bool] = Field(default=False, alias="telegram_adapter_debug")

    class Config:
        extra = "ignore"
        allow_population_by_field_name = True
