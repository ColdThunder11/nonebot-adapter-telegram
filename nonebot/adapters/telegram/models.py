from typing import Dict, List, Optional, Text, Union
from typing_extensions import Literal

from pydantic import BaseModel, root_validator
from enum import Enum


class MessageType(str, Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"

class MessageEntityType(str, Enum):
    mention = "mention"
    hashtag = "hashtag"
    cashtag = "cashtag"
    bot_command = "bot_command"
    url = "url"
    email = "email"
    phone_number = "phone_number"
    bold = "bold"
    italic = "italic"
    underline = "underline"
    strikethrough = "strikethrough"
    code = "code"
    pre = "pre"
    text_link = "text_link"
    text_mention = "text_mention"

class MessageUser(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
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
            values["from_"] = values["from"]
            del values["from"]
        return values
    result_id: str
    from_: MessageUser
    location: Optional[dict]
    inline_message_id: Optional[str]
    query: str


class LocationMessage(BaseModel):
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
    # not in document
    all_members_are_administrators: Optional[bool]
    # Returned only in getChat
    photo: Optional[ChatPhoto]
    bio: Optional[str]
    description: Optional[str]
    invite_link: Optional[str]
    pinned_message: Optional[Dict]  # type: MessageBody
    permissions: Optional[ChatPermissions]
    slow_mode_delay: Optional[int]
    message_auto_delete_time: Optional[int]
    sticker_set_name: Optional[str]
    can_set_sticker_set: Optional[bool]
    linked_chat_id: Optional[int]
    location: Optional[LocationMessage]


class ChatInviteLink(BaseModel):
    invite_link: str
    creator: MessageUser
    is_primary: bool
    is_revoked: bool
    expire_date: Optional[int]
    member_limit: Optional[int]

class ChatMember(BaseModel):
    status: str
    user: MessageUser


class ChatMemberOwner(ChatMember):
    status: str = "creator"
    is_anonymous: bool
    custom_title: str


class ChatMemberAdministrator(ChatMember):
    status: str = "administrator"
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_voice_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_messages: Optional[bool]
    can_edit_messages: Optional[bool]
    can_pin_messages: Optional[bool]
    custom_title: Optional[str]


class ChatMemberMember(ChatMember):
    status: str = "member"


class ChatMemberRestricted(ChatMember):
    status: str = "restricted"
    is_member: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_send_messages: bool
    can_send_media_messages: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    until_date: int


class ChatMemberLeft(ChatMember):
    status: str = "left"


class ChatMemberBanned(ChatMember):
    status: str = "kicked"


class ChatMemberUpdated(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    chat: MessageChat
    from_: MessageUser 
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: Optional[ChatInviteLink]

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



class Sticker(BaseModel):
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

class StickerSet(BaseModel):
    name: str
    title: str
    is_animated: bool
    contains_masks: bool
    stickers: List[Sticker]
    thumb: Optional[PhotoSizeItem]

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


class ContactMessage(BaseModel):
    phone_number: str
    first_name: str
    last_name: Optional[str]
    user_id: Optional[int]
    vcard: Optional[str]


class DiceMessage(BaseModel):
    emoji: str
    value: int


class GameMessage(BaseModel):
    title: str
    description: str
    photo: List[PhotoSizeItem]
    text: Optional[str]
    text_entities: Optional[List[MessageEntitiy]]
    animation: Optional[AnimationMessage]


class PollOption(BaseModel):
    text: str
    voter_count: str


class PollMessage(BaseModel):
    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: Optional[int]
    explanation: Optional[str]
    explanation_entities: Optional[List[MessageEntitiy]]
    open_period: Optional[int]
    close_date: Optional[int]


class VenueMessage(BaseModel):
    location: LocationMessage
    title: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]
    google_place_id: Optional[str]
    google_place_type: Optional[str]


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int


class InvoiceMessage(BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    shipping_address: Optional[ShippingAddress]


class SuccessfulPaymentMessage(BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]
    telegram_payment_charge_id: str
    provider_payment_charge_id: str

class PassportFile(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int

class EncryptedPassportElement(BaseModel):
    type: str
    data: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    files: Optional[List[PassportFile]]
    front_side: Optional[PassportFile]
    reverse_side: Optional[PassportFile]
    selfie: Optional[PassportFile]
    translation: Optional[List[PassportFile]]
    hash: str

class EncryptedCredentials(BaseModel):
    data: str
    hash: str
    secert: str

class PassportData(BaseModel):
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials

class ProximityAlertTriggered(BaseModel):
    traveler: MessageUser
    watcher: MessageUser
    distance: int

class VoiceChatStarted(BaseModel):
    pass

class VoiceChatScheduled(BaseModel):
    start_date: int

class VoiceChatEnded(BaseModel):
    duration: int

class VoiceChatParticipantsInvited(BaseModel):
    users: List[MessageUser]

class InlineKeyboardButton(BaseModel):  # 不完整
    text: str
    url: Optional[str]
    callback_data: Optional[str]

class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]]

class MessageBody(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    message_id: int
    from_: Optional[MessageUser]
    sender_chat: Optional[MessageChat]
    date: int
    chat: MessageChat
    forward_from: Optional[MessageUser]
    forward_from_chat: Optional[MessageChat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional[Dict]  # type: MessageBody
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
    sticker: Optional[Sticker]
    video: Optional[VideoMessage]
    video_note: Optional[VideoNoteMessage]
    voice: Optional[VoiceMessage]
    caption: Optional[str]
    caption_entities: Optional[List[MessageEntitiy]]
    contact: Optional[ContactMessage]
    dice: Optional[DiceMessage]
    game: Optional[GameMessage]
    poll: Optional[PollMessage]
    venue: Optional[VenueMessage]
    location: Optional[LocationMessage]
    new_chat_members: Optional[List[MessageUser]]
    left_chat_member: Optional[MessageUser]
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List[PhotoSizeItem]]
    delete_chat_photo: Optional[bool]
    group_chat_created: Optional[bool]
    supergroup_chat_created: Optional[bool]
    channel_chat_created: Optional[bool]
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged]
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    pinned_message: Optional[Dict]  # type: MessageBody
    invoice: Optional[InvoiceMessage]
    successful_payment: Optional[SuccessfulPaymentMessage]
    connected_website: Optional[str]
    passport_data: Optional[PassportData]
    proximity_alert_triggered: Optional[ProximityAlertTriggered]
    voice_chat_scheduled: Optional[VoiceChatScheduled]
    voice_chat_started: Optional[VoiceChatStarted]
    voice_chat_ended: Optional[VoiceChatEnded]
    voice_chat_participants_invited: Optional[VoiceChatParticipantsInvited]
    reply_markup: Optional[InlineKeyboardMarkup]

class CallbackQuery(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        values["from_"] = values["from"]
        del values["from"]
        return values
    id: str
    from_: MessageUser
    message: Optional[MessageBody]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]

class InlineQuery(BaseModel):
    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    id: str
    from_: MessageUser
    query: str
    offset: str
    chat_type: Optional[MessageType]
    location: Optional[LocationMessage]


class SendText(BaseModel):
    chat_id: Optional[Union[int, str]]
    text: str
    parse_mode: Optional[str]
    entities: Optional[List[MessageEntitiy]]
    disable_web_page_preview: Optional[bool]
    disable_notification: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[InlineKeyboardMarkup]


class SendPhoto(BaseModel):
    chat_id: Optional[Union[int, str]]
    photo: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntitiy]]
    disable_notification: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[InlineKeyboardMarkup]


class SendAudio(BaseModel):
    chat_id: Optional[Union[int, str]]
    audio: Optional[str]
    caption: Optional[str]
    parse_mode: Optional[str]
    caption_entities: Optional[List[MessageEntitiy]]
    duration: Optional[int]
    performer: Optional[str]
    title: Optional[str]
    thumb: Optional[str]
    disable_notification: Optional[bool]
    reply_to_message_id: Optional[int]
    allow_sending_without_reply: Optional[bool]
    reply_markup: Optional[InlineKeyboardMarkup]


class EditMessageText(BaseModel):
    chat_id: Optional[Union[int, str]]
    message_id: Optional[int]
    inline_message_id: Optional[str]
    text: str
    parse_mode: Optional[str]
    entities: Optional[List[MessageEntitiy]]
    disable_web_page_preview: Optional[bool]
    reply_markup: Optional[InlineKeyboardMarkup]
