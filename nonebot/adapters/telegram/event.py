from copy import Error
from enum import Enum
from re import S
from ssl import OP_ALL
from typing import Dict, List, Optional, Text, Union
from typing_extensions import Literal
from typing import Any
from xmlrpc.client import boolean
from pydantic import BaseModel, root_validator

from nonebot.typing import overrides
from nonebot.adapters import Event as BaseEvent

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

    #patch pydantic validate, ignore dict check(not recommand to use, just lazy) #For nb2 before https://github.com/nonebot/nonebot2/pull/876
    @classmethod
    @overrides(BaseModel)
    def validate(cls: BaseModel, value: Any) -> BaseModel:
        if isinstance(value, cls):
            if cls.__config__.copy_on_model_validation:
                return value._copy_and_set_values(value.__dict__, value.__fields_set__, deep=False)
            else:
                return value

        value = cls._enforce_dict_if_root(value)

        if isinstance(value, dict):
            return cls(**value)
        elif cls.__config__.orm_mode:
            return cls.from_orm(value)
        else:
            #ignore dict check, directly throw wrror
            raise TypeError()



class MessageEvent(Event):
    """消息事件，是Update结构的超集"""
    update_id: "int"
    message: Optional["MessageBody"]
    edited_message: Optional["MessageBody"]
    channel_post: Optional["MessageBody"]
    edited_channel_post: Optional["MessageBody"]
    inline_query: Optional["InlineQuery"]
    chosen_inline_result: Optional["ChosenInlineResult"]
    callback_query: Optional["CallbackQuery"]
    shipping_query: Optional["ShippingQuery"]
    pre_checkout_query: Optional["PreCheckoutQuery"]
    poll: Optional["Poll"]
    poll_answer: Optional["PollAnswer"]
    my_chat_member: Optional["ChatMemberUpdated"]
    chat_member: Optional["ChatMemberUpdated"]
    chat_join_request: Optional["ChatJoinRequest"]

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

    def get_message_struct_in_message(self, message: MessageBody) -> Message:
        if message.text:
            boolean
            return Message(message.text)
        data = {}
        if message.caption:
            data["caption"] = message.caption
        if message.photo:
            data.update(message.photo[0].dict())
            data["photo"] = message.photo[0].file_id
            return Message(MessageSegment("photo",data))
        elif message.document:
            data.update(message.document.dict())
            data["document"] = message.document.file_id
            return Message(MessageSegment("document",data))
        elif message.sticker:
            data.update(message.sticker.dict())
            data["sticker"] = message.sticker.file_id
            return Message(MessageSegment("sticker",data))
        elif message.voice:
            data.update(message.voice.dict())
            data["voice"] = message.voice.file_id
            return Message(MessageSegment("voice",data))
        elif message.audio:
            data.update(message.audio.dict())
            data["audio"] = message.audio.file_id
            return Message(MessageSegment("audio",data))
        elif message.animation:
            data.update(message.animation.dict())
            data["animation"] = message.animation.file_id
            return Message(MessageSegment("animation",data))
        elif message.video:
            data.update(message.video.dict())
            data["video"] = message.video.file_id
            return Message(MessageSegment("video",data))
        elif message.video_note:
            data.update(message.video_note.dict())
            data["video_note"] = message.video_note.file_id
            return Message(MessageSegment("video_note",data))
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
        return str(self.message.from_.id)

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

    # @overrides(Event)
    # def get_session_id(self) -> str:
    #    return f"group_{self.message.chat.id}_{self.message.from_.id}"


class CallbackQueryEvent(MessageEvent):
    """CallbackQuery消息"""

    #Infact,I think CallbackQuery should not be message, but treat it as message can make you easily build it into got
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
        return Message(MessageSegment("text",{"type": "callback_query", "text": self.callback_query.data}))


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

    def get_members_info(self) -> List[User]:
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

    def get_member_info(self) -> List[User]:
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

    def get_chat_photo(self) -> PhotoSize:
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


class VideoChatStartedEvent(MessageEvent):
    """视频聊天开始事件"""
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

    def get_voice_chat_started(self) -> VideoChatStarted:
        return self.message.video_chat_started


class VideoChatEndedEvent(MessageEvent):
    """视频聊天结束事件"""
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

    def get_voice_chat_ended(self) -> VideoChatEnded:
        return self.message.video_chat_ended
