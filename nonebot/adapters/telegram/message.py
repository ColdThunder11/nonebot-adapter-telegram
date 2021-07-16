from copy import copy
from typing import Any, Dict, List, Optional, Union, Mapping, Iterable

from nonebot.typing import overrides
from nonebot.adapters import Message as BaseMessage, MessageSegment as BaseMessageSegment

'''
文字：{"type": "text", "data": {"text": "123"}}
照片：{"type": "photo", "data": {"photo": List[PhotoSizeItem], "file": "file:///", "caption": "123"}}
文件：{"type": "file", "data": {"document": DocumentMessage}}
reply_markup：{"type": "markup", "data": {"type": "inline"(现在仅支持),"inline_keyboard":[{"text":"a"}]}}
'''                             
class MessageSegment(BaseMessageSegment):
    """
    telegram 协议 MessageSegment 适配。
    """

    @overrides(BaseMessageSegment)
    def __init__(self, type_: str, data: Dict[str, Any]) -> None:
        self.type = type_
        self.data = data
        #super().__init__(type=type_, data=data)

    @overrides(BaseMessageSegment)
    def __str__(self):
        if self.type == "text":
            return str(self.data["text"])
        return ""

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
    def text(text: str) -> "MessageSegment":
        """发送 ``text`` 类型消息"""
        return MessageSegment("text", {"text": text})
    
    @staticmethod
    def photo(file: str, caption: str = None):
        if caption:
            return MessageSegment("photo", {"file": file, "caption": caption})
        else:
            return MessageSegment("photo", {"file": file})
    #cqhttp兼容方法
    @staticmethod
    def image(file: str,
              type_: Optional[str] = None,
              cache: bool = True,
              proxy: bool = True,
              timeout: Optional[int] = None) -> "MessageSegment":
        return MessageSegment(
            "photo", {
                "file": file
            })
    #cqhttp兼容方法
    @staticmethod
    def at(user_id: Union[int, str]) -> "MessageSegment":
        return MessageSegment("at", {"id": str(user_id)})
    #cqhttp兼容方法
    @staticmethod
    def reply(id_: int) -> "MessageSegment":
        return MessageSegment("reply", {"id": str(id_)})
    @staticmethod
    def reply_markup(type: str, data:List):
        return MessageSegment("markup",{"type": type, "inline_keyboard": data})

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
