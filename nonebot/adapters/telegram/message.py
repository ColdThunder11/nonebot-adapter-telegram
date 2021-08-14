from copy import copy
from typing import Any, Dict, List, Type, Optional, Union, Mapping, Iterable

from functools import reduce

from pydantic.main import BaseModel
from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment
from .models import *

'''
文字：{"type": "text", "data": {"text": "123"}}
照片：{"type": "photo", "data": {"photo": "file:///", "caption": "123"}}
文件：{"type": "document", "data": {"file_name": "", "mime_type": "", "file": ""}}
贴纸：{"type": "sticker", "data": {"emoji": "😑", "is_animated": False, "file": ""}}
音频：{"type": "audio", "data": {"audio": "file:///", }}
去看tg文档吧，不想写了
reply_markup（仅发送）：{"type": "markup", "data": {"type": "inline"(现在仅支持),"inline_keyboard":[{"text":"a"}]}}
'''          


class MessageSegment(BaseMessageSegment["Message"]):
    """
    telegram 协议 MessageSegment 适配。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @overrides(BaseMessageSegment)
    def __init__(self, type_: str, data: Dict[str, Any]) -> None:
        self.type = type_
        self.data = data
        #super().__init__(type=type_, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self) -> str:
        if self.type == "text":
            return str(self.data["text"])
        type_ = self.type
        data = self.data.copy()
        params = ",".join(
            [f"{k}={str(v)}" for k, v in data.items() if v is not None])
        return f"[TG:{type_}{',' if params else ''}{params}]"

    @overrides(BaseMessageSegment)
    def __add__(self, other) -> "Message":
        return Message(self) + other

    @overrides(BaseMessageSegment)
    def __radd__(self, other) -> "Message":
        return Message(other) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"
    
    @staticmethod
    def text(text: str, **kwargs) -> "MessageSegment":
        """发送 ``text`` 类型消息"""
        ms_dict  = {}
        ms_dict["text"] = text
        ms_dict.update(kwargs)
        return MessageSegment("text", ms_dict)

    @staticmethod
    def photo(photo: str, caption: str = None, obj: SendPhoto = None, **kwargs) -> "MessageSegment":
        if obj:
            return MessageSegment("photo", obj.dict())
        ms_dict  = {}
        ms_dict["photo"] = photo
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("photo", ms_dict)

    @staticmethod
    def audio(audio: str, caption: str = None, obj: SendAudio = None, **kwargs) -> "MessageSegment":
        if obj:
            return MessageSegment("audio", obj.dict())
        ms_dict  = {}
        ms_dict["audio"] = audio
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("audio", ms_dict)

    @staticmethod
    def voice(voice: str, caption: str = None, **kwargs) -> "MessageSegment":
        ms_dict  = {}
        ms_dict["voice"] = voice
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("voice", ms_dict)

    @staticmethod
    def video(video: str, caption: str = None, **kwargs) -> "MessageSegment":
        ms_dict  = {}
        ms_dict["video"] = video
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("video", ms_dict)

    @staticmethod
    def animation(animation: str, caption: str = None, **kwargs) -> "MessageSegment":
        ms_dict  = {}
        ms_dict["animation"] = animation
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("animation", ms_dict)

    @staticmethod
    def document(document: str, caption: str = None, **kwargs) -> "MessageSegment":
        ms_dict  = {}
        ms_dict["document"] = document
        ms_dict.update(kwargs)
        if caption:
            ms_dict["caption"] = caption
        return MessageSegment("document", ms_dict)

    @staticmethod
    def reply_markup(type: str, inline_keyboard:List) -> "MessageSegment":
        return MessageSegment("markup",{"type": type, "inline_keyboard": inline_keyboard})

    @staticmethod
    def sticker(sticker: str, obj:StickerMessage = None, **kwargs) -> "MessageSegment":
        if obj:
            return MessageSegment("sticker", obj.dict())
        ms_dict  = {}
        ms_dict["sticker"] = sticker
        ms_dict.update(kwargs)
        return MessageSegment("sticker", ms_dict)

    #cqhttp兼容方法
    @staticmethod
    def image(file: str,
              type_: Optional[str] = None,
              cache: bool = True,
              proxy: bool = True,
              timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            "photo", {
                "photo": file
            })
    #cqhttp兼容方法
    @staticmethod
    def at(user_id: Union[int, str]) -> "MessageSegment":
        return MessageSegment("at", {"id": str(user_id)})
    #cqhttp兼容方法
    @staticmethod
    def reply(id_: int) -> "MessageSegment":
        return MessageSegment("reply", {"id": str(id_)})

class Message(BaseMessage):
    """
    telegram 协议 Message 适配。
    """

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping,
                   Iterable[Mapping]]) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping):
            yield MessageSegment(msg["type"], msg.get("data") or {})
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
        elif isinstance(msg, Iterable):
            for seg in msg:
                yield MessageSegment(seg["type"], seg.get("data") or {})

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        text = ""
        for ms in self:
            text += str(ms)
        return text
