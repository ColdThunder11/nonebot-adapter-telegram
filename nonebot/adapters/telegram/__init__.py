"""
telegram 协议适配
============================

"""

from .utils import log
from .bot import Bot
from .message import Message, MessageSegment
from .event import Event, MessageEvent, PrivateMessageEvent, GroupMessageEvent, CallbackQueryEvent
from .exception import (TelegramAdapterException, ApiNotAvailable, NetworkError,
                        ActionFailed)
