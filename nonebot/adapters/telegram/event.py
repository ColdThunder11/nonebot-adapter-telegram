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

class MessageType(str, Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"

class MessageUser(BaseModel):
    id: int
    is_bot: bool
    first_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]

class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]

class MaskPosition(BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float

class ChatPhoto(BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

class ChosenInlineResult(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["mfrom"] = values["from"]
            del values["from"]
        return values
    result_id: str
    mfrom: MessageUser
    location: Optional[dict]
    inline_message_id: Optional[str]
    query: str

class MessageLocation(BaseEvent):
    longitude: float
    latitude: float
    horizontal_accuracy: Optional[float]
    live_period: Optional[int]
    heading: Optional[int]
    proximity_alert_radius: Optional[int]

class MessageChat(BaseModel):
    id: int
    type: MessageType
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    #not in document
    all_members_are_administrators: Optional[bool]
    #Returned only in getChat
    photo: Optional[ChatPhoto]
    bio: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    pinned_message: Optional[Dict] # type: MessageBody
    permissions: Optional[ChatPermissions]
    slow_mode_delay: Optional[int]
    message_auto_delete_time: Optional[int]
    sticker_set_name: Optional[str]
    can_set_sticker_set: Optional[bool]
    linked_chat_id: Optional[int]
    location: Optional[MessageLocation]

class MessageEntitiy(BaseModel):
    offset: int
    length: int
    type: str
    url: Optional[str]
    user: Optional[MessageUser]
    language: Optional[str]

class InputMediaPhoto(BaseModel):
    type: str
    media: str
    caption: Optional[str]
    prase_mode: Optional[str]
    caption_entities: Optional[List[MessageEntitiy]]

class TextMessage(BaseModel):
    content: str

class PhotoSizeItem(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    width: int
    height: int

class AudioMessage(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str]
    title: Optional[str]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]
    thumb: Optional[PhotoSizeItem]

class AnimationMessage(BaseModel):
    file_name: Optional[str]
    mime_type: Optional[str]
    duration: int
    width: int
    height: int
    thumb: Optional[PhotoSizeItem]
    file_id: str
    file_unique_id: str
    file_size: Optional[int]

class DocumentMessage(BaseModel):
    file_name: str
    mime_type: str
    thumb: Optional[PhotoSizeItem]
    file_id: str
    file_unique_id: str
    file_size: int

class StickerMessage(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSizeItem]
    emoji: Optional[str]
    set_name: Optional[str]
    mask_position: Optional[MaskPosition]
    file_size: Optional[int]

class VideoMessage(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSizeItem]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]

class VideoNoteMessage(BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSizeItem]
    file_size: Optional[int]

class VoiceMessage(BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str]
    file_size: Optional[int]



class MessageBody(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["mfrom"] = values["from"]
            del values["from"]
        return values
    message_id: int
    mfrom: Optional[MessageUser]
    sender_chat: Optional[MessageChat]
    date: int
    chat: MessageChat
    forward_from: Optional[MessageUser]
    forward_from_chat: Optional[MessageChat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional[Dict] # type: MessageBody
    via_bot: Optional[MessageUser]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]
    entities: Optional[List[MessageEntitiy]]
    animation: Optional[AnimationMessage]
    audio: Optional[AudioMessage]
    document: Optional[DocumentMessage]
    photo: Optional[List[PhotoSizeItem]]
    sticker: Optional[StickerMessage]
    video: Optional[VideoMessage]
    video_note: Optional[VideoNoteMessage]
    voice: Optional[VoiceMessage]
    caption: Optional[str]
    caption_entities: Optional[List[MessageEntitiy]]
    new_chat_members: Optional[List[MessageUser]]
    left_chat_member: Optional[MessageUser]
    new_chat_title: Optional[str]
    


    
class CallbackQuery(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        values["mfrom"] = values["from"]
        del values["from"]
        return values
    id: str
    mfrom: MessageUser
    message: Optional[MessageBody]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]

class InlineQuery(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["mfrom"] = values["from"]
            del values["from"]
        return values
    id: str
    mfrom: MessageUser
    query: str
    offset: str
    chat_type: Optional[MessageType]
    location: Optional[MessageLocation]


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

    to_me: bool = True

    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "message"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.message.chat.type.name}"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.message.chat.type}] {self.message.chat.id} from {self.message.mfrom.id} "{self.message.text}"'

    @overrides(Event)
    def get_message(self) -> Message:
        if self.message.text:
            return Message(self.message.text)
        elif self.message.photo:
            if self.message.caption:
                return Message([{"type": "photo","data":{"photo":self.message.photo}},
                {"type": "text","data":{"text":self.message.caption}}])
            else:
                return Message([{"type": "photo","data":{"photo":self.message.photo}}])
        else:
            return None
        
    @overrides(Event)
    def get_plaintext(self) -> str:
        if self.message.text:
            return self.message.text
        #if self.message.photo:
        #    if self.message.caption:
        #        return self.message.caption
        return ""

    @overrides(Event)
    def get_user_id(self) -> str:
        return self.message.mfrom.id

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"{self.message.chat.id}_{self.message.mfrom.id}" 

    @overrides(Event)
    def is_tome(self) -> bool:
        return self.to_me

class PrivateMessageEvent(MessageEvent):
    pass

class GroupMessageEvent(MessageEvent):
    to_me = False
    #@overrides(MessageEvent)
    #def is_tome(self) -> bool:
    #    return self.isInAtList

    @overrides(Event)
    def get_session_id(self) -> str:
        return f"group_{self.message.chat.id}_{self.message.mfrom.id}" 

class CallbackQueryEvent(MessageEvent):
    @overrides(Event)
    def get_type(self):
        return "CallbackQuery"

    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.CallbackQuery"

    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_type()}] {self.callback_query.id} from {self.callback_query.mfrom.id} "{self.callback_query.data}"'
    
    @overrides(Event)
    def get_plaintext(self) -> str:
        return self.callback_query.data

    @overrides(Event)
    def get_message(self) -> Message:
        return Message([{"type": "markup","data":{"type": "inline"}}])

class NewChatMembersEvent(MessageEvent):
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"
    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.new_chat_members"
    @overrides(Event)
    def get_event_description(self) -> str:
        return f'Message[{self.get_type()}] {len(self.message.new_chat_members)} new member(s) to {self.message.chat.title}'
    @overrides(Event)
    def get_session_id(self) -> str:
        return f"group_new_member" 
    def get_member_info(self) -> List[MessageUser]:
        return self.message.new_chat_members

class LeafChatMemberEvent(MessageEvent):
    @overrides(Event)
    def get_type(self) -> Literal["message", "notice", "request", "meta_event"]:
        return "notice"
    @overrides(Event)
    def get_event_name(self) -> str:
        return f"{self.get_type()}.left_chat_member"
    @overrides(Event)
    def get_event_description(self) -> str:
        if self.message.left_chat_member.username:
            return f'Message[{self.get_type()}] {self.message.left_chat_member.username} leaf {self.message.chat.title}'
        else:
            return f'Message[{self.get_type()}] {self.message.left_chat_member.id} leaf {self.message.chat.title}'
    @overrides(Event)
    def get_session_id(self) -> str:
        return f"group_new_member" 
    def get_member_info(self) -> List[MessageUser]:
        return self.message.new_chat_members