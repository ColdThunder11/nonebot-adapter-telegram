from copy import Error
from enum import Enum
from re import S
from ssl import OP_ALL
from typing import Dict, List, Optional, Text, Union
from typing_extensions import Literal

from pydantic import BaseModel, root_validator

from nonebot.typing import overrides
from nonebot.adapters import Event as BaseEvent
from typing import Any

from .message import Message, MessageSegment
from .models import *


class Event(BaseEvent):
    """
    telegram协议事件。
    """

    @overrides(BaseEvent)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        raise ValueError("Event has no type!")

    @overrides(BaseEvent)
    def get_event_name(self) -> str:
        raise ValueError("Event has no name!")

    @overrides(BaseEvent)
    def get_event_description(self) -> str:
        raise ValueError("Event has no description!")

    @overrides(BaseEvent)
    def get_message(self) -> "Message":
        raise ValueError("Event has no message!")

    @overrides(BaseEvent)
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @overrides(BaseEvent)
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @overrides(BaseEvent)
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")

    @overrides(BaseEvent)
    def is_tome(self) -> bool:
        return True

class MessageEvent(Event):
    """消息事件"""
    update_id: int
    message: Optional[MessageBody]
    edited_message: Optional[MessageBody]
    channel_post: Optional[MessageBody]
    edited_channel_post: Optional[MessageBody]
    inline_query: Optional[InlineQuery]
    chosen_inline_result: Optional[ChosenInlineResult]
    callback_query: Optional[CallbackQuery]

    message_struct: Optional[Message]

    user_id: Optional[int]
    group_id: Optional[int]

    to_me: bool = True

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.message.chat.type.name}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.message.chat.type}] {self.message.message_id} from {self.message.from_.id} in {self.message.chat.id} "{self.get_plaintext()}"'

    def get_message_struct_in_message(self,message: MessageBody) -> Message:
        if message.text:
            return Message(message.text)
        data = {}
        if message.caption:
            data["caption"] = message.caption
        if message.photo:
            data.update(message.photo[0].dict())
            data["photo"] = message.photo[0].file_id
            return Message([{"type": "photo", "data": data}])
        elif message.document:
            data.update(message.document.dict())
            data["document"] = message.document.file_id
            return Message([{"type": "document", "data": data}])
        elif message.sticker:
            data.update(message.sticker.dict())
            data["sticker"] = message.sticker.file_id
            return Message([{"type": "sticker", "data": data}])
        elif message.voice:
            data.update(message.voice.dict())
            data["voice"] = message.voice.file_id
            return Message([{"type": "voice", "data": data}])
        elif message.audio:
            data.update(message.audio.dict())
            data["audio"] = message.audio.file_id
            return Message([{"type": "audio", "data": data}])
        elif message.animation:
            data.update(message.animation.dict())
            data["animation"] = message.animation.file_id
            return Message([{"type": "animation", "data": data}])
        elif message.video:
            data.update(message.video.dict())
            data["video"] = message.video.file_id
            return Message([{"type": "video", "data": data}])
        elif message.video_note:
            data.update(message.video_note.dict())
            data["video_note"] = message.video_note.file_id
            return Message([{"type": "video_note", "data": data}])
        return None

    def get_message_struct(self) -> Message:
        ret_msg: MessageBody = None
        if ret_msg := self.get_message_struct_in_message(self.message):
            return ret_msg
        elif ret_msg := self.get_message_struct_in_message(MessageBody.parse_obj(self.message.reply_to_message)):
            return ret_msg
        else:
            return Message("")

    @overrides(Event)
    def get_message(self) -> Message:
        if not self.message_struct:
            msg_struct: Message = self.get_message_struct()
            self.message_struct = msg_struct
        return self.message_struct

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.get_message().extract_plain_text()

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.message.from_.id

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}_{self.message.from_.id}"

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.to_me

class PrivateMessageEvent(MessageEvent):
    """私聊消息"""
    pass

class GroupMessageEvent(MessageEvent):
    """群聊消息"""
    to_me = False
    # @overrides(MessageEvent)
    # def is_tome(self) -> bool:
    #    return self.isInAtList

    #@overrides(Event)
    #def get_session_id(self) -> str:
    #    return f"group_{self.message.chat.id}_{self.message.from_.id}"

class CallbackQueryEvent(MessageEvent):
    """CallbackQuery消息"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.callback_query"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] {self.callback_query.id} from {self.callback_query.from_.id} "{self.callback_query.data}"'

    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.callback_query.data

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.callback_query.message.chat.id}_{self.callback_query.from_.id}"

    @overrides(Event)
    def get_message(self) -> Message:
        return Message([{"type": "text", "data": {"type": "callback_query", "text": self.callback_query.data}}])

class NewChatMembersEvent(MessageEvent):
    """入群事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.new_chat_members"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] {len(self.message.new_chat_members)} new member(s) to {self.message.chat.title}'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_members_info(self) -> List[MessageUser]:
        return self.message.new_chat_members

class LeafChatMemberEvent(MessageEvent):
    """退群事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.left_chat_member"

    @overrides(Event)
    def get_event_description(self) -> str:
        if self.message.left_chat_member.username:
            return f'Message[{self.get_event_name()}] {self.message.left_chat_member.username} leaf chat {self.message.chat.title}'
        else:
            return f'Message[{self.get_event_name()}] {self.message.left_chat_member.id} leaf chat {self.message.chat.title}'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_member_info(self) -> List[MessageUser]:
        return self.message.left_chat_member

class NewChatTitleEvent(MessageEvent):
    """群名（聊天标题）变更事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.new_chat_title"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] chat {self.message.chat.id} change title to {self.message.chat.title}'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_chat_name(self) -> str:
        return self.message.new_chat_title

class NewChatPhotoEvent(MessageEvent):
    """群头像（聊天头像）变更事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.new_chat_photo"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] chat {self.message.chat.id} change chat photo to {self.message.new_chat_photo[0].file_id}'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_chat_photo(self) -> PhotoSizeItem:
        return self.message.new_chat_photo[0]

class DeleteChatPhotoEvent(MessageEvent):
    """群头像（聊天头像）删除事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.delete_chat_photo"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] chat {self.message.chat.id} delete chat photo'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

class VoiceChatStartedEvent(MessageEvent):
    """语言聊天开始事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.voice_chat_started"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] chat {self.message.chat.id} start voice chat'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_voice_chat_started(self) -> VoiceChatStarted:
        return self.message.voice_chat_started

class VoiceChatEndedEvent(MessageEvent):
    """语言聊天结束事件"""
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.voice_chat_ended"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_event_name()}] chat {self.message.chat.id} start voice chat'

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}"

    def get_voice_chat_ended(self) -> VoiceChatEnded:
        return self.message.voice_chat_ended

