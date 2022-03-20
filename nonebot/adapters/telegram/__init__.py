"""
telegram 协议适配
============================

"""
import logging

from nonebot.log import LoguruHandler, logger

aiocache_logger = logging.getLogger("aiocache.serializers.serializers")
aiocache_logger.setLevel(logging.DEBUG)
aiocache_logger.handlers.clear()
aiocache_logger.addHandler(LoguruHandler())

from .bot import Bot
from .adapter import Adapter
from .message import Message, MessageSegment
from .event import Event, MessageEvent, PrivateMessageEvent, GroupMessageEvent, CallbackQueryEvent
from .exception import (TelegramAdapterException, ApiNotAvailable, NetworkError,
                        ActionFailed)
