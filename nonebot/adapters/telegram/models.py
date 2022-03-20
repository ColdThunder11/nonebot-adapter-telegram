
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

class Update(BaseModel):
    '''
    This object represents an incoming update.At most one of the optional parameters can be present in any given update.

    Arguments:
        update_id: The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This ID becomes especially handy if you're using Webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.
        message: Optional. New incoming message of any kind &#8212; text, photo, sticker, etc.
        edited_message: Optional. New version of a message that is known to the bot and was edited
        channel_post: Optional. New incoming channel post of any kind &#8212; text, photo, sticker, etc.
        edited_channel_post: Optional. New version of a channel post that is known to the bot and was edited
        inline_query: Optional. New incoming inline query
        chosen_inline_result: Optional. The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot.
        callback_query: Optional. New incoming callback query
        shipping_query: Optional. New incoming shipping query. Only for invoices with flexible price
        pre_checkout_query: Optional. New incoming pre-checkout query. Contains full information about checkout
        poll: Optional. New poll state. Bots receive only updates about stopped polls and polls, which are sent by the bot
        poll_answer: Optional. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself.
        my_chat_member: Optional. The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user.
        chat_member: Optional. A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify &#8220;chat_member&#8221; in the list of allowed_updates to receive these updates.
        chat_join_request: Optional. A request to join the chat has been sent. The bot must have the can_invite_users administrator right in the chat to receive these updates.
    '''
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


class User(BaseModel):
    '''
    This object represents a Telegram user or bot.

    Arguments:
        id: Unique identifier for this user or bot. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
        is_bot: True, if this user is a bot
        first_name: User's or bot's first name
        last_name: Optional. User's or bot's last name
        username: Optional. User's or bot's username
        language_code: Optional. IETF language tag of the user's language
        can_join_groups: Optional. True, if the bot can be invited to groups. Returned only in getMe.
        can_read_all_group_messages: Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
        supports_inline_queries: Optional. True, if the bot supports inline queries. Returned only in getMe.
    '''
    id: "int"
    is_bot: "bool"
    first_name: "str"
    last_name: Optional["str"]
    username: Optional["str"]
    language_code: Optional["str"]
    can_join_groups: Optional["bool"]
    can_read_all_group_messages: Optional["bool"]
    supports_inline_queries: Optional["bool"]


class Chat(BaseModel):
    '''
    This object represents a chat.

    Arguments:
        id: Unique identifier for this chat. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        type: Type of chat, can be either &#8220;private&#8221;, &#8220;group&#8221;, &#8220;supergroup&#8221; or &#8220;channel&#8221;
        title: Optional. Title, for supergroups, channels and group chats
        username: Optional. Username, for private chats, supergroups and channels if available
        first_name: Optional. First name of the other party in a private chat
        last_name: Optional. Last name of the other party in a private chat
        photo: Optional. Chat photo. Returned only in getChat.
        bio: Optional. Bio of the other party in a private chat. Returned only in getChat.
        has_private_forwards: Optional. True, if privacy settings of the other party in the private chat allows to use tg://user?id=&lt;user_id&gt; links only in chats with the user. Returned only in getChat.
        description: Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.
        invite_link: Optional. Primary invite link, for groups, supergroups and channel chats. Returned only in getChat.
        pinned_message: Optional. The most recent pinned message (by sending date). Returned only in getChat.
        permissions: Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        slow_mode_delay: Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user; in seconds. Returned only in getChat.
        message_auto_delete_time: Optional. The time after which all messages sent to the chat will be automatically deleted; in seconds. Returned only in getChat.
        has_protected_content: Optional. True, if messages from the chat can't be forwarded to other chats. Returned only in getChat.
        sticker_set_name: Optional. For supergroups, name of group sticker set. Returned only in getChat.
        can_set_sticker_set: Optional. True, if the bot can change the group sticker set. Returned only in getChat.
        linked_chat_id: Optional. Unique identifier for the linked chat, i.e. the discussion group identifier for a channel and vice versa; for supergroups and channel chats. This identifier may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier. Returned only in getChat.
        location: Optional. For supergroups, the location to which the supergroup is connected. Returned only in getChat.
    '''
    id: "int"
    type: "MessageType"
    title: Optional["str"]
    username: Optional["str"]
    first_name: Optional["str"]
    last_name: Optional["str"]
    photo: Optional["ChatPhoto"]
    bio: Optional["str"]
    has_private_forwards: Optional["bool"]
    description: Optional["str"]
    invite_link: Optional["str"]
    pinned_message: Optional["MessageBody"]
    permissions: Optional["ChatPermissions"]
    slow_mode_delay: Optional["int"]
    message_auto_delete_time: Optional["int"]
    has_protected_content: Optional["bool"]
    sticker_set_name: Optional["str"]
    can_set_sticker_set: Optional["bool"]
    linked_chat_id: Optional["int"]
    location: Optional["ChatLocation"]


class MessageBody(BaseModel):
    '''
    This object represents a message.

    Arguments:
        message_id: Unique message identifier inside this chat
        from_: Optional. Sender of the message; empty for messages sent to channels. For backward compatibility, the field contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
        sender_chat: Optional. Sender of the message, sent on behalf of a chat. For example, the channel itself for channel posts, the supergroup itself for messages from anonymous group administrators, the linked channel for messages automatically forwarded to the discussion group.  For backward compatibility, the field from contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
        date: Date the message was sent in Unix time
        chat: Conversation the message belongs to
        forwardfrom_: Optional. For forwarded messages, sender of the original message
        forwardfrom_chat: Optional. For messages forwarded from channels or from anonymous administrators, information about the original sender chat
        forwardfrom_message_id: Optional. For messages forwarded from channels, identifier of the original message in the channel
        forward_signature: Optional. For forwarded messages that were originally sent in channels or by an anonymous chat administrator, signature of the message sender if present
        forward_sender_name: Optional. Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
        forward_date: Optional. For forwarded messages, date the original message was sent in Unix time
        is_automatic_forward: Optional. True, if the message is a channel post that was automatically forwarded to the connected discussion group
        reply_to_message: Optional. For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
        via_bot: Optional. Bot through which the message was sent
        edit_date: Optional. Date the message was last edited in Unix time
        has_protected_content: Optional. True, if the message can't be forwarded
        media_group_id: Optional. The unique identifier of a media message group this message belongs to
        author_signature: Optional. Signature of the post author for messages in channels, or the custom title of an anonymous group administrator
        text: Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters
        entities: Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
        animation: Optional. Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set
        audio: Optional. Message is an audio file, information about the file
        document: Optional. Message is a general file, information about the file
        photo: Optional. Message is a photo, available sizes of the photo
        sticker: Optional. Message is a sticker, information about the sticker
        video: Optional. Message is a video, information about the video
        video_note: Optional. Message is a video note, information about the video message
        voice: Optional. Message is a voice message, information about the file
        caption: Optional. Caption for the animation, audio, document, photo, video or voice, 0-1024 characters
        caption_entities: Optional. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
        contact: Optional. Message is a shared contact, information about the contact
        dice: Optional. Message is a dice with random value
        game: Optional. Message is a game, information about the game. More about games &#187;
        poll: Optional. Message is a native poll, information about the poll
        venue: Optional. Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set
        location: Optional. Message is a shared location, information about the location
        new_chat_members: Optional. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
        left_chat_member: Optional. A member was removed from the group, information about them (this member may be the bot itself)
        new_chat_title: Optional. A chat title was changed to this value
        new_chat_photo: Optional. A chat photo was change to this value
        delete_chat_photo: Optional. Service message: the chat photo was deleted
        group_chat_created: Optional. Service message: the group has been created
        supergroup_chat_created: Optional. Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        channel_chat_created: Optional. Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
        message_auto_delete_timer_changed: Optional. Service message: auto-delete timer settings changed in the chat
        migrate_to_chat_id: Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        migratefrom_chat_id: Optional. The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        pinned_message: Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itself a reply.
        invoice: Optional. Message is an invoice for a payment, information about the invoice. More about payments &#187;
        successful_payment: Optional. Message is a service message about a successful payment, information about the payment. More about payments &#187;
        connected_website: Optional. The domain name of the website on which the user has logged in. More about Telegram Login &#187;
        passport_data: Optional. Telegram Passport data
        proximity_alert_triggered: Optional. Service message. A user in the chat triggered another user's proximity alert while sharing Live Location.
        voice_chat_scheduled: Optional. Service message: voice chat scheduled
        voice_chat_started: Optional. Service message: voice chat started
        voice_chat_ended: Optional. Service message: voice chat ended
        voice_chat_participants_invited: Optional. Service message: new participants invited to a voice chat
        reply_markup: Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    message_id: "int"
    from_: Optional["User"]
    sender_chat: Optional["Chat"]
    date: "int"
    chat: "Chat"
    forwardfrom_: Optional["User"]
    forwardfrom_chat: Optional["Chat"]
    forwardfrom_message_id: Optional["int"]
    forward_signature: Optional["str"]
    forward_sender_name: Optional["str"]
    forward_date: Optional["int"]
    is_automatic_forward: Optional["bool"]
    reply_to_message: Optional["MessageBody"]
    via_bot: Optional["User"]
    edit_date: Optional["int"]
    has_protected_content: Optional["bool"]
    media_group_id: Optional["str"]
    author_signature: Optional["str"]
    text: Optional["str"]
    entities: Optional[List["MessageEntity"]]
    animation: Optional["Animation"]
    audio: Optional["Audio"]
    document: Optional["Document"]
    photo: Optional[List["PhotoSize"]]
    sticker: Optional["Sticker"]
    video: Optional["Video"]
    video_note: Optional["VideoNote"]
    voice: Optional["Voice"]
    caption: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    contact: Optional["Contact"]
    dice: Optional["Dice"]
    game: Optional["Game"]
    poll: Optional["Poll"]
    venue: Optional["Venue"]
    location: Optional["Location"]
    new_chat_members: Optional[List["User"]]
    left_chat_member: Optional["User"]
    new_chat_title: Optional["str"]
    new_chat_photo: Optional[List["PhotoSize"]]
    delete_chat_photo: Optional["bool"]
    group_chat_created: Optional["bool"]
    supergroup_chat_created: Optional["bool"]
    channel_chat_created: Optional["bool"]
    message_auto_delete_timer_changed: Optional["MessageAutoDeleteTimerChanged"]
    migrate_to_chat_id: Optional["int"]
    migratefrom_chat_id: Optional["int"]
    pinned_message: Optional["MessageBody"]
    invoice: Optional["Invoice"]
    successful_payment: Optional["SuccessfulPayment"]
    connected_website: Optional["str"]
    passport_data: Optional["PassportData"]
    proximity_alert_triggered: Optional["ProximityAlertTriggered"]
    voice_chat_scheduled: Optional["VoiceChatScheduled"]
    voice_chat_started: Optional["VoiceChatStarted"]
    voice_chat_ended: Optional["VoiceChatEnded"]
    voice_chat_participants_invited: Optional["VoiceChatParticipantsInvited"]
    reply_markup: Optional["InlineKeyboardMarkup"]


class MessageId(BaseModel):
    '''
    This object represents a unique message identifier.

    Arguments:
        message_id: Unique message identifier
    '''
    message_id: "int"


class MessageEntity(BaseModel):
    '''
    This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc.

    Arguments:
        type: Type of the entity. Currently, can be &#8220;mention&#8221; (@username), &#8220;hashtag&#8221; (#hashtag), &#8220;cashtag&#8221; ($USD), &#8220;bot_command&#8221; (/start@jobs_bot), &#8220;url&#8221; (https://telegram.org), &#8220;email&#8221; (do-not-reply@telegram.org), &#8220;phone_number&#8221; (+1-212-555-0123), &#8220;bold&#8221; (bold text), &#8220;italic&#8221; (italic text), &#8220;underline&#8221; (underlined text), &#8220;strikethrough&#8221; (strikethrough text), &#8220;spoiler&#8221; (spoiler message), &#8220;code&#8221; (monowidth string), &#8220;pre&#8221; (monowidth block), &#8220;text_link&#8221; (for clickable text URLs), &#8220;text_mention&#8221; (for users without usernames)
        offset: Offset in UTF-16 code units to the start of the entity
        length: Length of the entity in UTF-16 code units
        url: Optional. For &#8220;text_link&#8221; only, url that will be opened after user taps on the text
        user: Optional. For &#8220;text_mention&#8221; only, the mentioned user
        language: Optional. For &#8220;pre&#8221; only, the programming language of the entity text
    '''
    type: "MessageEntityType"
    offset: "int"
    length: "int"
    url: Optional["str"]
    user: Optional["User"]
    language: Optional["str"]


class PhotoSize(BaseModel):
    '''
    This object represents one size of a photo or a file / sticker thumbnail.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: Photo width
        height: Photo height
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    width: "int"
    height: "int"
    file_size: Optional["int"]


class Animation(BaseModel):
    '''
    This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound).

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: Video width as defined by sender
        height: Video height as defined by sender
        duration: Duration of the video in seconds as defined by sender
        thumb: Optional. Animation thumbnail as defined by sender
        file_name: Optional. Original animation filename as defined by sender
        mime_type: Optional. MIME type of the file as defined by sender
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    width: "int"
    height: "int"
    duration: "int"
    thumb: Optional["PhotoSize"]
    file_name: Optional["str"]
    mime_type: Optional["str"]
    file_size: Optional["int"]


class Audio(BaseModel):
    '''
    This object represents an audio file to be treated as music by the Telegram clients.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        duration: Duration of the audio in seconds as defined by sender
        performer: Optional. Performer of the audio as defined by sender or by audio tags
        title: Optional. Title of the audio as defined by sender or by audio tags
        file_name: Optional. Original filename as defined by sender
        mime_type: Optional. MIME type of the file as defined by sender
        file_size: Optional. File size in bytes
        thumb: Optional. Thumbnail of the album cover to which the music file belongs
    '''
    file_id: "str"
    file_unique_id: "str"
    duration: "int"
    performer: Optional["str"]
    title: Optional["str"]
    file_name: Optional["str"]
    mime_type: Optional["str"]
    file_size: Optional["int"]
    thumb: Optional["PhotoSize"]


class Document(BaseModel):
    '''
    This object represents a general file (as opposed to photos, voice messages and audio files).

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        thumb: Optional. Document thumbnail as defined by sender
        file_name: Optional. Original filename as defined by sender
        mime_type: Optional. MIME type of the file as defined by sender
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    thumb: Optional["PhotoSize"]
    file_name: Optional["str"]
    mime_type: Optional["str"]
    file_size: Optional["int"]


class Video(BaseModel):
    '''
    This object represents a video file.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: Video width as defined by sender
        height: Video height as defined by sender
        duration: Duration of the video in seconds as defined by sender
        thumb: Optional. Video thumbnail
        file_name: Optional. Original filename as defined by sender
        mime_type: Optional. Mime type of a file as defined by sender
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    width: "int"
    height: "int"
    duration: "int"
    thumb: Optional["PhotoSize"]
    file_name: Optional["str"]
    mime_type: Optional["str"]
    file_size: Optional["int"]


class VideoNote(BaseModel):
    '''
    This object represents a video message (available in Telegram apps as of v.4.0).

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        length: Video width and height (diameter of the video message) as defined by sender
        duration: Duration of the video in seconds as defined by sender
        thumb: Optional. Video thumbnail
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    length: "int"
    duration: "int"
    thumb: Optional["PhotoSize"]
    file_size: Optional["int"]


class Voice(BaseModel):
    '''
    This object represents a voice note.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        duration: Duration of the audio in seconds as defined by sender
        mime_type: Optional. MIME type of the file as defined by sender
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    duration: "int"
    mime_type: Optional["str"]
    file_size: Optional["int"]


class Contact(BaseModel):
    '''
    This object represents a phone contact.

    Arguments:
        phone_number: Contact's phone number
        first_name: Contact's first name
        last_name: Optional. Contact's last name
        user_id: Optional. Contact's user identifier in Telegram. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
        vcard: Optional. Additional data about the contact in the form of a vCard
    '''
    phone_number: "str"
    first_name: "str"
    last_name: Optional["str"]
    user_id: Optional["int"]
    vcard: Optional["str"]


class Dice(BaseModel):
    '''
    This object represents an animated emoji that displays a random value.

    Arguments:
        emoji: Emoji on which the dice throw animation is based
        value: Value of the dice, 1-6 for &#8220;&#8221;, &#8220;&#8221; and &#8220;&#8221; base emoji, 1-5 for &#8220;&#8221; and &#8220;&#8221; base emoji, 1-64 for &#8220;&#8221; base emoji
    '''
    emoji: "str"
    value: "int"


class PollOption(BaseModel):
    '''
    This object contains information about one answer option in a poll.

    Arguments:
        text: Option text, 1-100 characters
        voter_count: Number of users that voted for this option
    '''
    text: "str"
    voter_count: "int"


class PollAnswer(BaseModel):
    '''
    This object represents an answer of a user in a non-anonymous poll.

    Arguments:
        poll_id: Unique poll identifier
        user: The user, who changed the answer to the poll
        option_ids: 0-based identifiers of answer options, chosen by the user. May be empty if the user retracted their vote.
    '''
    poll_id: "str"
    user: "User"
    option_ids: List["int"]


class Poll(BaseModel):
    '''
    This object contains information about a poll.

    Arguments:
        id: Unique poll identifier
        question: Poll question, 1-300 characters
        options: List of poll options
        total_voter_count: Total number of users that voted in the poll
        is_closed: True, if the poll is closed
        is_anonymous: True, if the poll is anonymous
        type: Poll type, currently can be &#8220;regular&#8221; or &#8220;quiz&#8221;
        allows_multiple_answers: True, if the poll allows multiple answers
        correct_option_id: Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
        explanation: Optional. Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll, 0-200 characters
        explanation_entities: Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation
        open_period: Optional. Amount of time in seconds the poll will be active after creation
        close_date: Optional. Point in time (Unix timestamp) when the poll will be automatically closed
    '''
    id: "str"
    question: "str"
    options: List["PollOption"]
    total_voter_count: "int"
    is_closed: "bool"
    is_anonymous: "bool"
    type: "str"
    allows_multiple_answers: "bool"
    correct_option_id: Optional["int"]
    explanation: Optional["str"]
    explanation_entities: Optional[List["MessageEntity"]]
    open_period: Optional["int"]
    close_date: Optional["int"]


class Location(BaseModel):
    '''
    This object represents a point on the map.

    Arguments:
        longitude: Longitude as defined by sender
        latitude: Latitude as defined by sender
        horizontal_accuracy: Optional. The radius of uncertainty for the location, measured in meters; 0-1500
        live_period: Optional. Time relative to the message sending date, during which the location can be updated; in seconds. For active live locations only.
        heading: Optional. The direction in which user is moving, in degrees; 1-360. For active live locations only.
        proximity_alert_radius: Optional. Maximum distance for proximity alerts about approaching another chat member, in meters. For sent live locations only.
    '''
    longitude: "float"
    latitude: "float"
    horizontal_accuracy: Optional["float"]
    live_period: Optional["int"]
    heading: Optional["int"]
    proximity_alert_radius: Optional["int"]


class Venue(BaseModel):
    '''
    This object represents a venue.

    Arguments:
        location: Venue location. Can't be a live location
        title: Name of the venue
        address: Address of the venue
        foursquare_id: Optional. Foursquare identifier of the venue
        foursquare_type: Optional. Foursquare type of the venue. (For example, &#8220;arts_entertainment/default&#8221;, &#8220;arts_entertainment/aquarium&#8221; or &#8220;food/icecream&#8221;.)
        google_place_id: Optional. Google Places identifier of the venue
        google_place_type: Optional. Google Places type of the venue. (See supported types.)
    '''
    location: "Location"
    title: "str"
    address: "str"
    foursquare_id: Optional["str"]
    foursquare_type: Optional["str"]
    google_place_id: Optional["str"]
    google_place_type: Optional["str"]


class ProximityAlertTriggered(BaseModel):
    '''
    This object represents the content of a service message, sent whenever a user in the chat triggers a proximity alert set by another user.

    Arguments:
        traveler: User that triggered the alert
        watcher: User that set the alert
        distance: The distance between the users
    '''
    traveler: "User"
    watcher: "User"
    distance: "int"


class MessageAutoDeleteTimerChanged(BaseModel):
    '''
    This object represents a service message about a change in auto-delete timer settings.

    Arguments:
        message_auto_delete_time: New auto-delete time for messages in the chat; in seconds
    '''
    message_auto_delete_time: "int"


class VoiceChatScheduled(BaseModel):
    '''
    This object represents a service message about a voice chat scheduled in the chat.

    Arguments:
        start_date: Point in time (Unix timestamp) when the voice chat is supposed to be started by a chat administrator
    '''
    start_date: "int"


class VoiceChatStarted(BaseModel):
    '''
    This object represents a service message about a voice chat started in the chat. Currently holds no information.

    Arguments:
    '''
pass

class VoiceChatEnded(BaseModel):
    '''
    This object represents a service message about a voice chat ended in the chat.

    Arguments:
        duration: Voice chat duration in seconds
    '''
    duration: "int"


class VoiceChatParticipantsInvited(BaseModel):
    '''
    This object represents a service message about new members invited to a voice chat.

    Arguments:
        users: Optional. New members that were invited to the voice chat
    '''
    users: Optional[List["User"]]


class UserProfilePhotos(BaseModel):
    '''
    This object represent a user's profile pictures.

    Arguments:
        total_count: Total number of profile pictures the target user has
        photos: Requested profile pictures (in up to 4 sizes each)
    '''
    total_count: "int"
    photos: List["PhotoSize"]


class File(BaseModel):
    '''
    This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot&lt;token&gt;/&lt;file_path&gt;. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile.

    Arguments:
    '''
pass

class ReplyKeyboardMarkup(BaseModel):
    '''
    This object represents a custom keyboard with reply options (see Introduction to bots for details and examples).

    Arguments:
        keyboard: Array of button rows, each represented by an Array of KeyboardButton objects
        resize_keyboard: Optional. Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to false, in which case the custom keyboard is always of the same height as the app's standard keyboard.
        one_time_keyboard: Optional. Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat &#8211; the user can press a special button in the input field to see the custom keyboard again. Defaults to false.
        input_field_placeholder: Optional. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters
        selective: Optional. Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.Example: A user requests to change the bot's language, bot replies to the request with a keyboard to select the new language. Other users in the group don't see the keyboard.
    '''
    keyboard: List["KeyboardButton"]
    resize_keyboard: Optional["bool"]
    one_time_keyboard: Optional["bool"]
    input_field_placeholder: Optional["str"]
    selective: Optional["bool"]


class KeyboardButton(BaseModel):
    '''
    This object represents one button of the reply keyboard. For simple text buttons String can be used instead of this object to specify text of the button. Optional fields request_contact, request_location, and request_poll are mutually exclusive.

    Arguments:
        text: Text of the button. If none of the optional fields are used, it will be sent as a message when the button is pressed
        request_contact: Optional. If True, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only
        request_location: Optional. If True, the user's current location will be sent when the button is pressed. Available in private chats only
        request_poll: Optional. If specified, the user will be asked to create a poll and send it to the bot when the button is pressed. Available in private chats only
    '''
    text: "str"
    request_contact: Optional["bool"]
    request_location: Optional["bool"]
    request_poll: Optional["KeyboardButtonPollType"]


class KeyboardButtonPollType(BaseModel):
    '''
    This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed.

    Arguments:
        type: Optional. If quiz is passed, the user will be allowed to create only polls in the quiz mode. If regular is passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type.
    '''
    type: Optional["str"]


class ReplyKeyboardRemove(BaseModel):
    '''
    Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup).

    Arguments:
        remove_keyboard: Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use one_time_keyboard in ReplyKeyboardMarkup)
        selective: Optional. Use this parameter if you want to remove the keyboard for specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.Example: A user votes in a poll, bot returns confirmation message in reply to the vote and removes the keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet.
    '''
    remove_keyboard: "bool"
    selective: Optional["bool"]


class InlineKeyboardMarkup(BaseModel):
    '''
    This object represents an inline keyboard that appears right next to the message it belongs to.

    Arguments:
        inline_keyboard: Array of button rows, each represented by an Array of InlineKeyboardButton objects
    '''
    inline_keyboard: List["InlineKeyboardButton"]


class InlineKeyboardButton(BaseModel):
    '''
    This object represents one button of an inline keyboard. You must use exactly one of the optional fields.

    Arguments:
        text: Label text on the button
        url: Optional. HTTP or tg:// url to be opened when the button is pressed. Links tg://user?id=&lt;user_id&gt; can be used to mention a user by their ID without using a username, if this is allowed by their privacy settings.
        login_url: Optional. An HTTP URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.
        callback_data: Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
        switch_inline_query: Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot's username and the specified inline query in the input field. Can be empty, in which case just the bot's username will be inserted.Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private chat with it. Especially useful when combined with switch_pm&#8230; actions &#8211; in this case the user will be automatically returned to the chat they switched from, skipping the chat selection screen.
        switch_inline_query_current_chat: Optional. If set, pressing the button will insert the bot's username and the specified inline query in the current chat's input field. Can be empty, in which case only the bot's username will be inserted.This offers a quick way for the user to open your bot in inline mode in the same chat &#8211; good for selecting something from multiple options.
        callback_game: Optional. Description of the game that will be launched when the user presses the button.NOTE: This type of button must always be the first button in the first row.
        pay: Optional. Specify True, to send a Pay button.NOTE: This type of button must always be the first button in the first row and can only be used in invoice messages.
    '''
    text: "str"
    url: Optional["str"]
    login_url: Optional["LoginUrl"]
    callback_data: Optional["str"]
    switch_inline_query: Optional["str"]
    switch_inline_query_current_chat: Optional["str"]
    callback_game: Optional["CallbackGame"]
    pay: Optional["bool"]


class LoginUrl(BaseModel):
    '''
    This object represents a parameter of the inline keyboard button used to automatically authorize a user. Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:

    Arguments:
    '''
pass

class CallbackQuery(BaseModel):
    '''
    This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.

    Arguments:
        id: Unique identifier for this query
        from_: Sender
        message: Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
        inline_message_id: Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        chat_instance: Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
        data: Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
        game_short_name: Optional. Short name of a Game to be returned, serves as the unique identifier for the game
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    id: "str"
    from_: "User"
    message: Optional["MessageBody"]
    inline_message_id: Optional["str"]
    chat_instance: "str"
    data: Optional["str"]
    game_short_name: Optional["str"]


class ForceReply(BaseModel):
    '''
    Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot's message and tapped 'Reply'). This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to sacrifice privacy mode.

    Arguments:
        force_reply: Shows reply interface to the user, as if they manually selected the bot's message and tapped 'Reply'
        input_field_placeholder: Optional. The placeholder to be shown in the input field when the reply is active; 1-64 characters
        selective: Optional. Use this parameter if you want to force reply from specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
    '''
    force_reply: "bool"
    input_field_placeholder: Optional["str"]
    selective: Optional["bool"]


class ChatPhoto(BaseModel):
    '''
    This object represents a chat photo.

    Arguments:
        small_file_id: File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        small_file_unique_id: Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        big_file_id: File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        big_file_unique_id: Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    '''
    small_file_id: "str"
    small_file_unique_id: "str"
    big_file_id: "str"
    big_file_unique_id: "str"


class ChatInviteLink(BaseModel):
    '''
    Represents an invite link for a chat.

    Arguments:
        invite_link: The invite link. If the link was created by another chat administrator, then the second part of the link will be replaced with &#8220;&#8230;&#8221;.
        creator: Creator of the link
        creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators
        is_primary: True, if the link is primary
        is_revoked: True, if the link is revoked
        name: Optional. Invite link name
        expire_date: Optional. Point in time (Unix timestamp) when the link will expire or has been expired
        member_limit: Optional. Maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
        pending_join_request_count: Optional. Number of pending join requests created using this link
    '''
    invite_link: "str"
    creator: "User"
    creates_join_request: "bool"
    is_primary: "bool"
    is_revoked: "bool"
    name: Optional["str"]
    expire_date: Optional["int"]
    member_limit: Optional["int"]
    pending_join_request_count: Optional["int"]


class ChatMember(BaseModel):
    '''
    This object contains information about one member of a chat. Currently, the following 6 types of chat members are supported:

    Arguments:
    '''
pass

class ChatMemberOwner(BaseModel):
    '''
    Represents a chat member that owns the chat and has all administrator privileges.

    Arguments:
        status: The member's status in the chat, always &#8220;creator&#8221;
        user: Information about the user
        is_anonymous: True, if the user's presence in the chat is hidden
        custom_title: Optional. Custom title for this user
    '''
    status: "str"
    user: "User"
    is_anonymous: "bool"
    custom_title: Optional["str"]


class ChatMemberAdministrator(BaseModel):
    '''
    Represents a chat member that has some additional privileges.

    Arguments:
        status: The member's status in the chat, always &#8220;administrator&#8221;
        user: Information about the user
        can_be_edited: True, if the bot is allowed to edit administrator privileges of that user
        is_anonymous: True, if the user's presence in the chat is hidden
        can_manage_chat: True, if the administrator can access the chat event log, chat statistics, message statistics in channels, see channel members, see anonymous administrators in supergroups and ignore slow mode. Implied by any other administrator privilege
        can_delete_messages: True, if the administrator can delete messages of other users
        can_manage_voice_chats: True, if the administrator can manage voice chats
        can_restrict_members: True, if the administrator can restrict, ban or unban chat members
        can_promote_members: True, if the administrator can add new administrators with a subset of their own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by the user)
        can_change_info: True, if the user is allowed to change the chat title, photo and other settings
        can_invite_users: True, if the user is allowed to invite new users to the chat
        can_post_messages: Optional. True, if the administrator can post in the channel; channels only
        can_edit_messages: Optional. True, if the administrator can edit messages of other users and can pin messages; channels only
        can_pin_messages: Optional. True, if the user is allowed to pin messages; groups and supergroups only
        custom_title: Optional. Custom title for this user
    '''
    status: "str"
    user: "User"
    can_be_edited: "bool"
    is_anonymous: "bool"
    can_manage_chat: "bool"
    can_delete_messages: "bool"
    can_manage_voice_chats: "bool"
    can_restrict_members: "bool"
    can_promote_members: "bool"
    can_change_info: "bool"
    can_invite_users: "bool"
    can_post_messages: Optional["bool"]
    can_edit_messages: Optional["bool"]
    can_pin_messages: Optional["bool"]
    custom_title: Optional["str"]


class ChatMemberMember(BaseModel):
    '''
    Represents a chat member that has no additional privileges or restrictions.

    Arguments:
        status: The member's status in the chat, always &#8220;member&#8221;
        user: Information about the user
    '''
    status: "str"
    user: "User"


class ChatMemberRestricted(BaseModel):
    '''
    Represents a chat member that is under certain restrictions in the chat. Supergroups only.

    Arguments:
        status: The member's status in the chat, always &#8220;restricted&#8221;
        user: Information about the user
        is_member: True, if the user is a member of the chat at the moment of the request
        can_change_info: True, if the user is allowed to change the chat title, photo and other settings
        can_invite_users: True, if the user is allowed to invite new users to the chat
        can_pin_messages: True, if the user is allowed to pin messages
        can_send_messages: True, if the user is allowed to send text messages, contacts, locations and venues
        can_send_media_messages: True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes
        can_send_polls: True, if the user is allowed to send polls
        can_send_other_messages: True, if the user is allowed to send animations, games, stickers and use inline bots
        can_add_web_page_previews: True, if the user is allowed to add web page previews to their messages
        until_date: Date when restrictions will be lifted for this user; unix time. If 0, then the user is restricted forever
    '''
    status: "str"
    user: "User"
    is_member: "bool"
    can_change_info: "bool"
    can_invite_users: "bool"
    can_pin_messages: "bool"
    can_send_messages: "bool"
    can_send_media_messages: "bool"
    can_send_polls: "bool"
    can_send_other_messages: "bool"
    can_add_web_page_previews: "bool"
    until_date: "int"


class ChatMemberLeft(BaseModel):
    '''
    Represents a chat member that isn't currently a member of the chat, but may join it themselves.

    Arguments:
        status: The member's status in the chat, always &#8220;left&#8221;
        user: Information about the user
    '''
    status: "str"
    user: "User"


class ChatMemberBanned(BaseModel):
    '''
    Represents a chat member that was banned in the chat and can't return to the chat or view chat messages.

    Arguments:
        status: The member's status in the chat, always &#8220;kicked&#8221;
        user: Information about the user
        until_date: Date when restrictions will be lifted for this user; unix time. If 0, then the user is banned forever
    '''
    status: "str"
    user: "User"
    until_date: "int"


class ChatMemberUpdated(BaseModel):
    '''
    This object represents changes in the status of a chat member.

    Arguments:
        chat: Chat the user belongs to
        from_: Performer of the action, which resulted in the change
        date: Date the change was done in Unix time
        old_chat_member: Previous information about the chat member
        new_chat_member: New information about the chat member
        invite_link: Optional. Chat invite link, which was used by the user to join the chat; for joining by invite link events only.
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    chat: "Chat"
    from_: "User"
    date: "int"
    old_chat_member: "ChatMember"
    new_chat_member: "ChatMember"
    invite_link: Optional["ChatInviteLink"]


class ChatJoinRequest(BaseModel):
    '''
    Represents a join request sent to a chat.

    Arguments:
        chat: Chat to which the request was sent
        from_: User that sent the join request
        date: Date the request was sent in Unix time
        bio: Optional. Bio of the user.
        invite_link: Optional. Chat invite link that was used by the user to send the join request
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    chat: "Chat"
    from_: "User"
    date: "int"
    bio: Optional["str"]
    invite_link: Optional["ChatInviteLink"]


class ChatPermissions(BaseModel):
    '''
    Describes actions that a non-administrator user is allowed to take in a chat.

    Arguments:
        can_send_messages: Optional. True, if the user is allowed to send text messages, contacts, locations and venues
        can_send_media_messages: Optional. True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies can_send_messages
        can_send_polls: Optional. True, if the user is allowed to send polls, implies can_send_messages
        can_send_other_messages: Optional. True, if the user is allowed to send animations, games, stickers and use inline bots, implies can_send_media_messages
        can_add_web_page_previews: Optional. True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages
        can_change_info: Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups
        can_invite_users: Optional. True, if the user is allowed to invite new users to the chat
        can_pin_messages: Optional. True, if the user is allowed to pin messages. Ignored in public supergroups
    '''
    can_send_messages: Optional["bool"]
    can_send_media_messages: Optional["bool"]
    can_send_polls: Optional["bool"]
    can_send_other_messages: Optional["bool"]
    can_add_web_page_previews: Optional["bool"]
    can_change_info: Optional["bool"]
    can_invite_users: Optional["bool"]
    can_pin_messages: Optional["bool"]


class ChatLocation(BaseModel):
    '''
    Represents a location to which a chat is connected.

    Arguments:
        location: The location to which the supergroup is connected. Can't be a live location.
        address: Location address; 1-64 characters, as defined by the chat owner
    '''
    location: "Location"
    address: "str"


class BotCommand(BaseModel):
    '''
    This object represents a bot command.

    Arguments:
        command: Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores.
        description: Description of the command; 1-256 characters.
    '''
    command: "str"
    description: "str"


class BotCommandScope(BaseModel):
    '''
    This object represents the scope to which bot commands are applied. Currently, the following 7 scopes are supported:

    Arguments:
    '''
pass

class BotCommandScopeDefault(BaseModel):
    '''
    Represents the default scope of bot commands. Default commands are used if no commands with a narrower scope are specified for the user.

    Arguments:
        type: Scope type, must be default
    '''
    type: "str"


class BotCommandScopeAllPrivateChats(BaseModel):
    '''
    Represents the scope of bot commands, covering all private chats.

    Arguments:
        type: Scope type, must be all_private_chats
    '''
    type: "str"


class BotCommandScopeAllGroupChats(BaseModel):
    '''
    Represents the scope of bot commands, covering all group and supergroup chats.

    Arguments:
        type: Scope type, must be all_group_chats
    '''
    type: "str"


class BotCommandScopeAllChatAdministrators(BaseModel):
    '''
    Represents the scope of bot commands, covering all group and supergroup chat administrators.

    Arguments:
        type: Scope type, must be all_chat_administrators
    '''
    type: "str"


class BotCommandScopeChat(BaseModel):
    '''
    Represents the scope of bot commands, covering a specific chat.

    Arguments:
        type: Scope type, must be chat
        chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    '''
    type: "str"
    chat_id: Union[int, str]


class BotCommandScopeChatAdministrators(BaseModel):
    '''
    Represents the scope of bot commands, covering all administrators of a specific group or supergroup chat.

    Arguments:
        type: Scope type, must be chat_administrators
        chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
    '''
    type: "str"
    chat_id: Union[int, str]


class BotCommandScopeChatMember(BaseModel):
    '''
    Represents the scope of bot commands, covering a specific member of a group or supergroup chat.

    Arguments:
        type: Scope type, must be chat_member
        chat_id: Unique identifier for the target chat or username of the target supergroup (in the format @supergroupusername)
        user_id: Unique identifier of the target user
    '''
    type: "str"
    chat_id: Union[int, str]
    user_id: "int"


class ResponseParameters(BaseModel):
    '''
    Contains information about why a request was unsuccessful.

    Arguments:
        migrate_to_chat_id: Optional. The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        retry_after: Optional. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated
    '''
    migrate_to_chat_id: Optional["int"]
    retry_after: Optional["int"]


class InputMedia(BaseModel):
    '''
    This object represents the content of a media message to be sent. It should be one of

    Arguments:
    '''
pass

class InputMediaPhoto(BaseModel):
    '''
    Represents a photo to be sent.

    Arguments:
        type: Type of the result, must be photo
        media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass &#8220;attach://&lt;file_attach_name&gt;&#8221; to upload a new one using multipart/form-data under &lt;file_attach_name&gt; name. More info on Sending Files &#187;
        caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
    '''
    type: "str"
    media: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]


class InputMediaVideo(BaseModel):
    '''
    Represents a video to be sent.

    Arguments:
        type: Type of the result, must be video
        media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass &#8220;attach://&lt;file_attach_name&gt;&#8221; to upload a new one using multipart/form-data under &lt;file_attach_name&gt; name. More info on Sending Files &#187;
        thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass &#8220;attach://&lt;file_attach_name&gt;&#8221; if the thumbnail was uploaded using multipart/form-data under &lt;file_attach_name&gt;. More info on Sending Files &#187;
        caption: Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the video caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        width: Optional. Video width
        height: Optional. Video height
        duration: Optional. Video duration in seconds
        supports_streaming: Optional. Pass True, if the uploaded video is suitable for streaming
    '''
    type: "str"
    media: "str"
    thumb: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    width: Optional["int"]
    height: Optional["int"]
    duration: Optional["int"]
    supports_streaming: Optional["bool"]


class InputMediaAnimation(BaseModel):
    '''
    Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent.

    Arguments:
        type: Type of the result, must be animation
        media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass &#8220;attach://&lt;file_attach_name&gt;&#8221; to upload a new one using multipart/form-data under &lt;file_attach_name&gt; name. More info on Sending Files &#187;
        thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass &#8220;attach://&lt;file_attach_name&gt;&#8221; if the thumbnail was uploaded using multipart/form-data under &lt;file_attach_name&gt;. More info on Sending Files &#187;
        caption: Optional. Caption of the animation to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the animation caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        width: Optional. Animation width
        height: Optional. Animation height
        duration: Optional. Animation duration in seconds
    '''
    type: "str"
    media: "str"
    thumb: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    width: Optional["int"]
    height: Optional["int"]
    duration: Optional["int"]


class InputMediaAudio(BaseModel):
    '''
    Represents an audio file to be treated as music to be sent.

    Arguments:
        type: Type of the result, must be audio
        media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass &#8220;attach://&lt;file_attach_name&gt;&#8221; to upload a new one using multipart/form-data under &lt;file_attach_name&gt; name. More info on Sending Files &#187;
        thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass &#8220;attach://&lt;file_attach_name&gt;&#8221; if the thumbnail was uploaded using multipart/form-data under &lt;file_attach_name&gt;. More info on Sending Files &#187;
        caption: Optional. Caption of the audio to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the audio caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        duration: Optional. Duration of the audio in seconds
        performer: Optional. Performer of the audio
        title: Optional. Title of the audio
    '''
    type: "str"
    media: "str"
    thumb: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    duration: Optional["int"]
    performer: Optional["str"]
    title: Optional["str"]


class InputMediaDocument(BaseModel):
    '''
    Represents a general file to be sent.

    Arguments:
        type: Type of the result, must be document
        media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass &#8220;attach://&lt;file_attach_name&gt;&#8221; to upload a new one using multipart/form-data under &lt;file_attach_name&gt; name. More info on Sending Files &#187;
        thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass &#8220;attach://&lt;file_attach_name&gt;&#8221; if the thumbnail was uploaded using multipart/form-data under &lt;file_attach_name&gt;. More info on Sending Files &#187;
        caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the document caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        disable_content_type_detection: Optional. Disables automatic server-side content type detection for files uploaded using multipart/form-data. Always True, if the document is sent as part of an album.
    '''
    type: "str"
    media: "str"
    thumb: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    disable_content_type_detection: Optional["bool"]


class Sticker(BaseModel):
    '''
    This object represents a sticker.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        width: Sticker width
        height: Sticker height
        is_animated: True, if the sticker is animated
        is_video: True, if the sticker is a video sticker
        thumb: Optional. Sticker thumbnail in the .WEBP or .JPG format
        emoji: Optional. Emoji associated with the sticker
        set_name: Optional. Name of the sticker set to which the sticker belongs
        mask_position: Optional. For mask stickers, the position where the mask should be placed
        file_size: Optional. File size in bytes
    '''
    file_id: "str"
    file_unique_id: "str"
    width: "int"
    height: "int"
    is_animated: "bool"
    is_video: "bool"
    thumb: Optional["PhotoSize"]
    emoji: Optional["str"]
    set_name: Optional["str"]
    mask_position: Optional["MaskPosition"]
    file_size: Optional["int"]


class StickerSet(BaseModel):
    '''
    This object represents a sticker set.

    Arguments:
        name: Sticker set name
        title: Sticker set title
        is_animated: True, if the sticker set contains animated stickers
        is_video: True, if the sticker set contains video stickers
        contains_masks: True, if the sticker set contains masks
        stickers: List of all set stickers
        thumb: Optional. Sticker set thumbnail in the .WEBP, .TGS, or .WEBM format
    '''
    name: "str"
    title: "str"
    is_animated: "bool"
    is_video: "bool"
    contains_masks: "bool"
    stickers: List["Sticker"]
    thumb: Optional["PhotoSize"]


class MaskPosition(BaseModel):
    '''
    This object describes the position on faces where a mask should be placed by default.

    Arguments:
        point: The part of the face relative to which the mask should be placed. One of &#8220;forehead&#8221;, &#8220;eyes&#8221;, &#8220;mouth&#8221;, or &#8220;chin&#8221;.
        x_shift: Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
        y_shift: Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
        scale: Mask scaling coefficient. For example, 2.0 means double size.
    '''
    point: "str"
    x_shift: "float"
    y_shift: "float"
    scale: "float"


class sendSticker(BaseModel):
    '''
    Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.

    Arguments:
    '''
pass

class InlineQuery(BaseModel):
    '''
    This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results.

    Arguments:
        id: Unique identifier for this query
        from_: Sender
        query: Text of the query (up to 256 characters)
        offset: Offset of the results to be returned, can be controlled by the bot
        chat_type: Optional. Type of the chat, from which the inline query was sent. Can be either &#8220;sender&#8221; for a private chat with the inline query sender, &#8220;private&#8221;, &#8220;group&#8221;, &#8220;supergroup&#8221;, or &#8220;channel&#8221;. The chat type should be always known for requests sent from official clients and most third-party clients, unless the request was sent from a secret chat
        location: Optional. Sender location, only for bots that request user location
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    id: "str"
    from_: "User"
    query: "str"
    offset: "str"
    chat_type: Optional["str"]
    location: Optional["Location"]


class InlineQueryResult(BaseModel):
    '''
    This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:

    Arguments:
    '''
pass

class InlineQueryResultArticle(BaseModel):
    '''
    Represents a link to an article or web page.

    Arguments:
        type: Type of the result, must be article
        id: Unique identifier for this result, 1-64 Bytes
        title: Title of the result
        input_message_content: Content of the message to be sent
        reply_markup: Optional. Inline keyboard attached to the message
        url: Optional. URL of the result
        hide_url: Optional. Pass True, if you don't want the URL to be shown in the message
        description: Optional. Short description of the result
        thumb_url: Optional. Url of the thumbnail for the result
        thumb_width: Optional. Thumbnail width
        thumb_height: Optional. Thumbnail height
    '''
    type: "str"
    id: "str"
    title: "str"
    input_message_content: "InputMessageContent"
    reply_markup: Optional["InlineKeyboardMarkup"]
    url: Optional["str"]
    hide_url: Optional["bool"]
    description: Optional["str"]
    thumb_url: Optional["str"]
    thumb_width: Optional["int"]
    thumb_height: Optional["int"]


class InlineQueryResultPhoto(BaseModel):
    '''
    Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.

    Arguments:
        type: Type of the result, must be photo
        id: Unique identifier for this result, 1-64 bytes
        photo_url: A valid URL of the photo. Photo must be in JPEG format. Photo size must not exceed 5MB
        thumb_url: URL of the thumbnail for the photo
        photo_width: Optional. Width of the photo
        photo_height: Optional. Height of the photo
        title: Optional. Title for the result
        description: Optional. Short description of the result
        caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the photo
    '''
    type: "str"
    id: "str"
    photo_url: "str"
    thumb_url: "str"
    photo_width: Optional["int"]
    photo_height: Optional["int"]
    title: Optional["str"]
    description: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultGif(BaseModel):
    '''
    Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

    Arguments:
        type: Type of the result, must be gif
        id: Unique identifier for this result, 1-64 bytes
        gif_url: A valid URL for the GIF file. File size must not exceed 1MB
        gif_width: Optional. Width of the GIF
        gif_height: Optional. Height of the GIF
        gif_duration: Optional. Duration of the GIF in seconds
        thumb_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
        thumb_mime_type: Optional. MIME type of the thumbnail, must be one of &#8220;image/jpeg&#8221;, &#8220;image/gif&#8221;, or &#8220;video/mp4&#8221;. Defaults to &#8220;image/jpeg&#8221;
        title: Optional. Title for the result
        caption: Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the GIF animation
    '''
    type: "str"
    id: "str"
    gif_url: "str"
    gif_width: Optional["int"]
    gif_height: Optional["int"]
    gif_duration: Optional["int"]
    thumb_url: "str"
    thumb_mime_type: Optional["str"]
    title: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultMpeg4Gif(BaseModel):
    '''
    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). By default, this animated MPEG-4 file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

    Arguments:
        type: Type of the result, must be mpeg4_gif
        id: Unique identifier for this result, 1-64 bytes
        mpeg4_url: A valid URL for the MP4 file. File size must not exceed 1MB
        mpeg4_width: Optional. Video width
        mpeg4_height: Optional. Video height
        mpeg4_duration: Optional. Video duration in seconds
        thumb_url: URL of the static (JPEG or GIF) or animated (MPEG4) thumbnail for the result
        thumb_mime_type: Optional. MIME type of the thumbnail, must be one of &#8220;image/jpeg&#8221;, &#8220;image/gif&#8221;, or &#8220;video/mp4&#8221;. Defaults to &#8220;image/jpeg&#8221;
        title: Optional. Title for the result
        caption: Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the video animation
    '''
    type: "str"
    id: "str"
    mpeg4_url: "str"
    mpeg4_width: Optional["int"]
    mpeg4_height: Optional["int"]
    mpeg4_duration: Optional["int"]
    thumb_url: "str"
    thumb_mime_type: Optional["str"]
    title: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultVideo(BaseModel):
    '''
    Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.

    Arguments:
    '''
pass

class InlineQueryResultAudio(BaseModel):
    '''
    Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.

    Arguments:
        type: Type of the result, must be audio
        id: Unique identifier for this result, 1-64 bytes
        audio_url: A valid URL for the audio file
        title: Title
        caption: Optional. Caption, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the audio caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        performer: Optional. Performer
        audio_duration: Optional. Audio duration in seconds
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the audio
    '''
    type: "str"
    id: "str"
    audio_url: "str"
    title: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    performer: Optional["str"]
    audio_duration: Optional["int"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultVoice(BaseModel):
    '''
    Represents a link to a voice recording in an .OGG container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message.

    Arguments:
        type: Type of the result, must be voice
        id: Unique identifier for this result, 1-64 bytes
        voice_url: A valid URL for the voice recording
        title: Recording title
        caption: Optional. Caption, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the voice message caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        voice_duration: Optional. Recording duration in seconds
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the voice recording
    '''
    type: "str"
    id: "str"
    voice_url: "str"
    title: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    voice_duration: Optional["int"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultDocument(BaseModel):
    '''
    Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.

    Arguments:
        type: Type of the result, must be document
        id: Unique identifier for this result, 1-64 bytes
        title: Title for the result
        caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the document caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        document_url: A valid URL for the file
        mime_type: Mime type of the content of the file, either &#8220;application/pdf&#8221; or &#8220;application/zip&#8221;
        description: Optional. Short description of the result
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the file
        thumb_url: Optional. URL of the thumbnail (JPEG only) for the file
        thumb_width: Optional. Thumbnail width
        thumb_height: Optional. Thumbnail height
    '''
    type: "str"
    id: "str"
    title: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    document_url: "str"
    mime_type: "str"
    description: Optional["str"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]
    thumb_url: Optional["str"]
    thumb_width: Optional["int"]
    thumb_height: Optional["int"]


class InlineQueryResultLocation(BaseModel):
    '''
    Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.

    Arguments:
        type: Type of the result, must be location
        id: Unique identifier for this result, 1-64 Bytes
        latitude: Location latitude in degrees
        longitude: Location longitude in degrees
        title: Location title
        horizontal_accuracy: Optional. The radius of uncertainty for the location, measured in meters; 0-1500
        live_period: Optional. Period in seconds for which the location can be updated, should be between 60 and 86400.
        heading: Optional. For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        proximity_alert_radius: Optional. For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the location
        thumb_url: Optional. Url of the thumbnail for the result
        thumb_width: Optional. Thumbnail width
        thumb_height: Optional. Thumbnail height
    '''
    type: "str"
    id: "str"
    latitude: "float"
    longitude: "float"
    title: "str"
    horizontal_accuracy: Optional["float"]
    live_period: Optional["int"]
    heading: Optional["int"]
    proximity_alert_radius: Optional["int"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]
    thumb_url: Optional["str"]
    thumb_width: Optional["int"]
    thumb_height: Optional["int"]


class InlineQueryResultVenue(BaseModel):
    '''
    Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.

    Arguments:
        type: Type of the result, must be venue
        id: Unique identifier for this result, 1-64 Bytes
        latitude: Latitude of the venue location in degrees
        longitude: Longitude of the venue location in degrees
        title: Title of the venue
        address: Address of the venue
        foursquare_id: Optional. Foursquare identifier of the venue if known
        foursquare_type: Optional. Foursquare type of the venue, if known. (For example, &#8220;arts_entertainment/default&#8221;, &#8220;arts_entertainment/aquarium&#8221; or &#8220;food/icecream&#8221;.)
        google_place_id: Optional. Google Places identifier of the venue
        google_place_type: Optional. Google Places type of the venue. (See supported types.)
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the venue
        thumb_url: Optional. Url of the thumbnail for the result
        thumb_width: Optional. Thumbnail width
        thumb_height: Optional. Thumbnail height
    '''
    type: "str"
    id: "str"
    latitude: "float"
    longitude: "float"
    title: "str"
    address: "str"
    foursquare_id: Optional["str"]
    foursquare_type: Optional["str"]
    google_place_id: Optional["str"]
    google_place_type: Optional["str"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]
    thumb_url: Optional["str"]
    thumb_width: Optional["int"]
    thumb_height: Optional["int"]


class InlineQueryResultContact(BaseModel):
    '''
    Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.

    Arguments:
        type: Type of the result, must be contact
        id: Unique identifier for this result, 1-64 Bytes
        phone_number: Contact's phone number
        first_name: Contact's first name
        last_name: Optional. Contact's last name
        vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the contact
        thumb_url: Optional. Url of the thumbnail for the result
        thumb_width: Optional. Thumbnail width
        thumb_height: Optional. Thumbnail height
    '''
    type: "str"
    id: "str"
    phone_number: "str"
    first_name: "str"
    last_name: Optional["str"]
    vcard: Optional["str"]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]
    thumb_url: Optional["str"]
    thumb_width: Optional["int"]
    thumb_height: Optional["int"]


class InlineQueryResultGame(BaseModel):
    '''
    Represents a Game.

    Arguments:
        type: Type of the result, must be game
        id: Unique identifier for this result, 1-64 bytes
        game_short_name: Short name of the game
        reply_markup: Optional. Inline keyboard attached to the message
    '''
    type: "str"
    id: "str"
    game_short_name: "str"
    reply_markup: Optional["InlineKeyboardMarkup"]


class InlineQueryResultCachedPhoto(BaseModel):
    '''
    Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.

    Arguments:
        type: Type of the result, must be photo
        id: Unique identifier for this result, 1-64 bytes
        photo_file_id: A valid file identifier of the photo
        title: Optional. Title for the result
        description: Optional. Short description of the result
        caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the photo
    '''
    type: "str"
    id: "str"
    photo_file_id: "str"
    title: Optional["str"]
    description: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedGif(BaseModel):
    '''
    Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with specified content instead of the animation.

    Arguments:
        type: Type of the result, must be gif
        id: Unique identifier for this result, 1-64 bytes
        gif_file_id: A valid file identifier for the GIF file
        title: Optional. Title for the result
        caption: Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the GIF animation
    '''
    type: "str"
    id: "str"
    gif_file_id: "str"
    title: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedMpeg4Gif(BaseModel):
    '''
    Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

    Arguments:
        type: Type of the result, must be mpeg4_gif
        id: Unique identifier for this result, 1-64 bytes
        mpeg4_file_id: A valid file identifier for the MP4 file
        title: Optional. Title for the result
        caption: Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the video animation
    '''
    type: "str"
    id: "str"
    mpeg4_file_id: "str"
    title: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedSticker(BaseModel):
    '''
    Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.

    Arguments:
        type: Type of the result, must be sticker
        id: Unique identifier for this result, 1-64 bytes
        sticker_file_id: A valid file identifier of the sticker
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the sticker
    '''
    type: "str"
    id: "str"
    sticker_file_id: "str"
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedDocument(BaseModel):
    '''
    Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file.

    Arguments:
        type: Type of the result, must be document
        id: Unique identifier for this result, 1-64 bytes
        title: Title for the result
        document_file_id: A valid file identifier for the file
        description: Optional. Short description of the result
        caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the document caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the file
    '''
    type: "str"
    id: "str"
    title: "str"
    document_file_id: "str"
    description: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedVideo(BaseModel):
    '''
    Represents a link to a video file stored on the Telegram servers. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.

    Arguments:
        type: Type of the result, must be video
        id: Unique identifier for this result, 1-64 bytes
        video_file_id: A valid file identifier for the video file
        title: Title for the result
        description: Optional. Short description of the result
        caption: Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the video caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the video
    '''
    type: "str"
    id: "str"
    video_file_id: "str"
    title: "str"
    description: Optional["str"]
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedVoice(BaseModel):
    '''
    Represents a link to a voice message stored on the Telegram servers. By default, this voice message will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the voice message.

    Arguments:
        type: Type of the result, must be voice
        id: Unique identifier for this result, 1-64 bytes
        voice_file_id: A valid file identifier for the voice message
        title: Voice message title
        caption: Optional. Caption, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the voice message caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the voice message
    '''
    type: "str"
    id: "str"
    voice_file_id: "str"
    title: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InlineQueryResultCachedAudio(BaseModel):
    '''
    Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.

    Arguments:
        type: Type of the result, must be audio
        id: Unique identifier for this result, 1-64 bytes
        audio_file_id: A valid file identifier for the audio file
        caption: Optional. Caption, 0-1024 characters after entities parsing
        parse_mode: Optional. Mode for parsing entities in the audio caption. See formatting options for more details.
        caption_entities: Optional. List of special entities that appear in the caption, which can be specified instead of parse_mode
        reply_markup: Optional. Inline keyboard attached to the message
        input_message_content: Optional. Content of the message to be sent instead of the audio
    '''
    type: "str"
    id: "str"
    audio_file_id: "str"
    caption: Optional["str"]
    parse_mode: Optional["str"]
    caption_entities: Optional[List["MessageEntity"]]
    reply_markup: Optional["InlineKeyboardMarkup"]
    input_message_content: Optional["InputMessageContent"]


class InputMessageContent(BaseModel):
    '''
    This object represents the content of a message to be sent as a result of an inline query. Telegram clients currently support the following 5 types:

    Arguments:
    '''
pass

class InputTextMessageContent(BaseModel):
    '''
    Represents the content of a text message to be sent as the result of an inline query.

    Arguments:
        message_text: Text of the message to be sent, 1-4096 characters
        parse_mode: Optional. Mode for parsing entities in the message text. See formatting options for more details.
        entities: Optional. List of special entities that appear in message text, which can be specified instead of parse_mode
        disable_web_page_preview: Optional. Disables link previews for links in the sent message
    '''
    message_text: "str"
    parse_mode: Optional["str"]
    entities: Optional[List["MessageEntity"]]
    disable_web_page_preview: Optional["bool"]


class InputLocationMessageContent(BaseModel):
    '''
    Represents the content of a location message to be sent as the result of an inline query.

    Arguments:
        latitude: Latitude of the location in degrees
        longitude: Longitude of the location in degrees
        horizontal_accuracy: Optional. The radius of uncertainty for the location, measured in meters; 0-1500
        live_period: Optional. Period in seconds for which the location can be updated, should be between 60 and 86400.
        heading: Optional. For live locations, a direction in which the user is moving, in degrees. Must be between 1 and 360 if specified.
        proximity_alert_radius: Optional. For live locations, a maximum distance for proximity alerts about approaching another chat member, in meters. Must be between 1 and 100000 if specified.
    '''
    latitude: "float"
    longitude: "float"
    horizontal_accuracy: Optional["float"]
    live_period: Optional["int"]
    heading: Optional["int"]
    proximity_alert_radius: Optional["int"]


class InputVenueMessageContent(BaseModel):
    '''
    Represents the content of a venue message to be sent as the result of an inline query.

    Arguments:
        latitude: Latitude of the venue in degrees
        longitude: Longitude of the venue in degrees
        title: Name of the venue
        address: Address of the venue
        foursquare_id: Optional. Foursquare identifier of the venue, if known
        foursquare_type: Optional. Foursquare type of the venue, if known. (For example, &#8220;arts_entertainment/default&#8221;, &#8220;arts_entertainment/aquarium&#8221; or &#8220;food/icecream&#8221;.)
        google_place_id: Optional. Google Places identifier of the venue
        google_place_type: Optional. Google Places type of the venue. (See supported types.)
    '''
    latitude: "float"
    longitude: "float"
    title: "str"
    address: "str"
    foursquare_id: Optional["str"]
    foursquare_type: Optional["str"]
    google_place_id: Optional["str"]
    google_place_type: Optional["str"]


class InputContactMessageContent(BaseModel):
    '''
    Represents the content of a contact message to be sent as the result of an inline query.

    Arguments:
        phone_number: Contact's phone number
        first_name: Contact's first name
        last_name: Optional. Contact's last name
        vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
    '''
    phone_number: "str"
    first_name: "str"
    last_name: Optional["str"]
    vcard: Optional["str"]


class InputInvoiceMessageContent(BaseModel):
    '''
    Represents the content of an invoice message to be sent as the result of an inline query.

    Arguments:
        title: Product name, 1-32 characters
        description: Product description, 1-255 characters
        payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.
        provider_token: Payment provider token, obtained via Botfather
        currency: Three-letter ISO 4217 currency code, see more on currencies
        prices: Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        max_tip_amount: Optional. The maximum accepted amount for tips in the smallest units of the currency (integer, not float/double). For example, for a maximum tip of US$ 1.45 pass max_tip_amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0
        suggested_tip_amounts: Optional. A JSON-serialized array of suggested amounts of tip in the smallest units of the currency (integer, not float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed max_tip_amount.
        provider_data: Optional. A JSON-serialized object for data about the invoice, which will be shared with the payment provider. A detailed description of the required fields should be provided by the payment provider.
        photo_url: Optional. URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
        photo_size: Optional. Photo size
        photo_width: Optional. Photo width
        photo_height: Optional. Photo height
        need_name: Optional. Pass True, if you require the user's full name to complete the order
        need_phone_number: Optional. Pass True, if you require the user's phone number to complete the order
        need_email: Optional. Pass True, if you require the user's email address to complete the order
        need_shipping_address: Optional. Pass True, if you require the user's shipping address to complete the order
        send_phone_number_to_provider: Optional. Pass True, if user's phone number should be sent to provider
        send_email_to_provider: Optional. Pass True, if user's email address should be sent to provider
        is_flexible: Optional. Pass True, if the final price depends on the shipping method
    '''
    title: "str"
    description: "str"
    payload: "str"
    provider_token: "str"
    currency: "str"
    prices: List["LabeledPrice"]
    max_tip_amount: Optional["int"]
    suggested_tip_amounts: Optional[List["int"]]
    provider_data: Optional["str"]
    photo_url: Optional["str"]
    photo_size: Optional["int"]
    photo_width: Optional["int"]
    photo_height: Optional["int"]
    need_name: Optional["bool"]
    need_phone_number: Optional["bool"]
    need_email: Optional["bool"]
    need_shipping_address: Optional["bool"]
    send_phone_number_to_provider: Optional["bool"]
    send_email_to_provider: Optional["bool"]
    is_flexible: Optional["bool"]


class ChosenInlineResult(BaseModel):
    '''
    Represents a result of an inline query that was chosen by the user and sent to their chat partner.

    Arguments:
        result_id: The unique identifier for the result that was chosen
        from_: The user that chose the result
        location: Optional. Sender location, only for bots that require user location
        inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message. Will be also received in callback queries and can be used to edit the message.
        query: The query that was used to obtain the result
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    result_id: "str"
    from_: "User"
    location: Optional["Location"]
    inline_message_id: Optional["str"]
    query: "str"


class LabeledPrice(BaseModel):
    '''
    This object represents a portion of the price for goods or services.

    Arguments:
        label: Portion label
        amount: Price of the product in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    '''
    label: "str"
    amount: "int"


class Invoice(BaseModel):
    '''
    This object contains basic information about an invoice.

    Arguments:
        title: Product name
        description: Product description
        start_parameter: Unique bot deep-linking parameter that can be used to generate this invoice
        currency: Three-letter ISO 4217 currency code
        total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
    '''
    title: "str"
    description: "str"
    start_parameter: "str"
    currency: "str"
    total_amount: "int"


class ShippingAddress(BaseModel):
    '''
    This object represents a shipping address.

    Arguments:
        country_code: ISO 3166-1 alpha-2 country code
        state: State, if applicable
        city: City
        street_line1: First line for the address
        street_line2: Second line for the address
        post_code: Address post code
    '''
    country_code: "str"
    state: "str"
    city: "str"
    street_line1: "str"
    street_line2: "str"
    post_code: "str"


class OrderInfo(BaseModel):
    '''
    This object represents information about an order.

    Arguments:
        name: Optional. User name
        phone_number: Optional. User's phone number
        email: Optional. User email
        shipping_address: Optional. User shipping address
    '''
    name: Optional["str"]
    phone_number: Optional["str"]
    email: Optional["str"]
    shipping_address: Optional["ShippingAddress"]


class ShippingOption(BaseModel):
    '''
    This object represents one shipping option.

    Arguments:
        id: Shipping option identifier
        title: Option title
        prices: List of price portions
    '''
    id: "str"
    title: "str"
    prices: List["LabeledPrice"]


class SuccessfulPayment(BaseModel):
    '''
    This object contains basic information about a successful payment.

    Arguments:
        currency: Three-letter ISO 4217 currency code
        total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        invoice_payload: Bot specified invoice payload
        shipping_option_id: Optional. Identifier of the shipping option chosen by the user
        order_info: Optional. Order info provided by the user
        telegram_payment_charge_id: Telegram payment identifier
        provider_payment_charge_id: Provider payment identifier
    '''
    currency: "str"
    total_amount: "int"
    invoice_payload: "str"
    shipping_option_id: Optional["str"]
    order_info: Optional["OrderInfo"]
    telegram_payment_charge_id: "str"
    provider_payment_charge_id: "str"


class ShippingQuery(BaseModel):
    '''
    This object contains information about an incoming shipping query.

    Arguments:
        id: Unique query identifier
        from_: User who sent the query
        invoice_payload: Bot specified invoice payload
        shipping_address: User specified shipping address
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    id: "str"
    from_: "User"
    invoice_payload: "str"
    shipping_address: "ShippingAddress"


class PreCheckoutQuery(BaseModel):
    '''
    This object contains information about an incoming pre-checkout query.

    Arguments:
        id: Unique query identifier
        from_: User who sent the query
        currency: Three-letter ISO 4217 currency code
        total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        invoice_payload: Bot specified invoice payload
        shipping_option_id: Optional. Identifier of the shipping option chosen by the user
        order_info: Optional. Order info provided by the user
    '''

    @root_validator(pre=True)
    def gen_message(cls, values: dict):
        if "from" in values:
            values["from_"] = values["from"]
            del values["from"]
        return values
    id: "str"
    from_: "User"
    currency: "str"
    total_amount: "int"
    invoice_payload: "str"
    shipping_option_id: Optional["str"]
    order_info: Optional["OrderInfo"]


class PassportData(BaseModel):
    '''
    Contains information about Telegram Passport data shared with the bot by the user.

    Arguments:
        data: Array with information about documents and other Telegram Passport elements that was shared with the bot
        credentials: Encrypted credentials required to decrypt the data
    '''
    data: List["EncryptedPassportElement"]
    credentials: "EncryptedCredentials"


class PassportFile(BaseModel):
    '''
    This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.

    Arguments:
        file_id: Identifier for this file, which can be used to download or reuse the file
        file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        file_size: File size in bytes
        file_date: Unix time when the file was uploaded
    '''
    file_id: "str"
    file_unique_id: "str"
    file_size: "int"
    file_date: "int"


class EncryptedPassportElement(BaseModel):
    '''
    Contains information about documents or other Telegram Passport elements shared with the bot by the user.

    Arguments:
        type: Element type. One of &#8220;personal_details&#8221;, &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;, &#8220;address&#8221;, &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221;, &#8220;temporary_registration&#8221;, &#8220;phone_number&#8221;, &#8220;email&#8221;.
        data: Optional. Base64-encoded encrypted Telegram Passport element data provided by the user, available for &#8220;personal_details&#8221;, &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221; and &#8220;address&#8221; types. Can be decrypted and verified using the accompanying EncryptedCredentials.
        phone_number: Optional. User's verified phone number, available only for &#8220;phone_number&#8221; type
        email: Optional. User's verified email address, available only for &#8220;email&#8221; type
        files: Optional. Array of encrypted files with documents provided by the user, available for &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221; and &#8220;temporary_registration&#8221; types. Files can be decrypted and verified using the accompanying EncryptedCredentials.
        front_side: Optional. Encrypted file with the front side of the document, provided by the user. Available for &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221; and &#8220;internal_passport&#8221;. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        reverse_side: Optional. Encrypted file with the reverse side of the document, provided by the user. Available for &#8220;driver_license&#8221; and &#8220;identity_card&#8221;. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        selfie: Optional. Encrypted file with the selfie of the user holding a document, provided by the user; available for &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221; and &#8220;internal_passport&#8221;. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        translation: Optional. Array of encrypted files with translated versions of documents provided by the user. Available if requested for &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;, &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221; and &#8220;temporary_registration&#8221; types. Files can be decrypted and verified using the accompanying EncryptedCredentials.
        hash: Base64-encoded element hash for using in PassportElementErrorUnspecified
    '''
    type: "str"
    data: Optional["str"]
    phone_number: Optional["str"]
    email: Optional["str"]
    files: Optional[List["PassportFile"]]
    front_side: Optional["PassportFile"]
    reverse_side: Optional["PassportFile"]
    selfie: Optional["PassportFile"]
    translation: Optional[List["PassportFile"]]
    hash: "str"


class EncryptedCredentials(BaseModel):
    '''
    Contains data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes.

    Arguments:
        data: Base64-encoded encrypted JSON-serialized data with unique user's payload, data hashes and secrets required for EncryptedPassportElement decryption and authentication
        hash: Base64-encoded data hash for data authentication
        secret: Base64-encoded secret, encrypted with the bot's public RSA key, required for data decryption
    '''
    data: "str"
    hash: "str"
    secret: "str"


class PassportElementError(BaseModel):
    '''
    This object represents an error in the Telegram Passport element which was submitted that should be resolved by the user. It should be one of:

    Arguments:
    '''
pass

class PassportElementErrorDataField(BaseModel):
    '''
    Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes.

    Arguments:
        source: Error source, must be data
        type: The section of the user's Telegram Passport which has the error, one of &#8220;personal_details&#8221;, &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;, &#8220;address&#8221;
        field_name: Name of the data field which has the error
        data_hash: Base64-encoded data hash
        message: Error message
    '''
    source: "str"
    type: "str"
    field_name: "str"
    data_hash: "str"
    message: "str"


class PassportElementErrorFrontSide(BaseModel):
    '''
    Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes.

    Arguments:
        source: Error source, must be front_side
        type: The section of the user's Telegram Passport which has the issue, one of &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;
        file_hash: Base64-encoded hash of the file with the front side of the document
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hash: "str"
    message: "str"


class PassportElementErrorReverseSide(BaseModel):
    '''
    Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes.

    Arguments:
        source: Error source, must be reverse_side
        type: The section of the user's Telegram Passport which has the issue, one of &#8220;driver_license&#8221;, &#8220;identity_card&#8221;
        file_hash: Base64-encoded hash of the file with the reverse side of the document
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hash: "str"
    message: "str"


class PassportElementErrorSelfie(BaseModel):
    '''
    Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.

    Arguments:
        source: Error source, must be selfie
        type: The section of the user's Telegram Passport which has the issue, one of &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;
        file_hash: Base64-encoded hash of the file with the selfie
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hash: "str"
    message: "str"


class PassportElementErrorFile(BaseModel):
    '''
    Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes.

    Arguments:
        source: Error source, must be file
        type: The section of the user's Telegram Passport which has the issue, one of &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221;, &#8220;temporary_registration&#8221;
        file_hash: Base64-encoded file hash
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hash: "str"
    message: "str"


class PassportElementErrorFiles(BaseModel):
    '''
    Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes.

    Arguments:
        source: Error source, must be files
        type: The section of the user's Telegram Passport which has the issue, one of &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221;, &#8220;temporary_registration&#8221;
        file_hashes: List of base64-encoded file hashes
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hashes: List["str"]
    message: "str"


class PassportElementErrorTranslationFile(BaseModel):
    '''
    Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes.

    Arguments:
        source: Error source, must be translation_file
        type: Type of element of the user's Telegram Passport which has the issue, one of &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;, &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221;, &#8220;temporary_registration&#8221;
        file_hash: Base64-encoded file hash
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hash: "str"
    message: "str"


class PassportElementErrorTranslationFiles(BaseModel):
    '''
    Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change.

    Arguments:
        source: Error source, must be translation_files
        type: Type of element of the user's Telegram Passport which has the issue, one of &#8220;passport&#8221;, &#8220;driver_license&#8221;, &#8220;identity_card&#8221;, &#8220;internal_passport&#8221;, &#8220;utility_bill&#8221;, &#8220;bank_statement&#8221;, &#8220;rental_agreement&#8221;, &#8220;passport_registration&#8221;, &#8220;temporary_registration&#8221;
        file_hashes: List of base64-encoded file hashes
        message: Error message
    '''
    source: "str"
    type: "str"
    file_hashes: List["str"]
    message: "str"


class PassportElementErrorUnspecified(BaseModel):
    '''
    Represents an issue in an unspecified place. The error is considered resolved when new data is added.

    Arguments:
        source: Error source, must be unspecified
        type: Type of element of the user's Telegram Passport which has the issue
        element_hash: Base64-encoded element hash
        message: Error message
    '''
    source: "str"
    type: "str"
    element_hash: "str"
    message: "str"


class Game(BaseModel):
    '''
    This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers.

    Arguments:
        title: Title of the game
        description: Description of the game
        photo: Photo that will be displayed in the game message in chats.
        text: Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
        text_entities: Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc.
        animation: Optional. Animation that will be displayed in the game message in chats. Upload via BotFather
    '''
    title: "str"
    description: "str"
    photo: List["PhotoSize"]
    text: Optional["str"]
    text_entities: Optional[List["MessageEntity"]]
    animation: Optional["Animation"]


class CallbackGame(BaseModel):
    '''
    A placeholder, currently holds no information. Use BotFather to set up your game.

    Arguments:
    '''
pass

class GameHighScore(BaseModel):
    '''
    This object represents one row of the high scores table for a game.

    Arguments:
        position: Position in high score table for the game
        user: User
        score: Score
    '''
    position: "int"
    user: "User"
    score: "int"

Update.update_forward_refs()
Chat.update_forward_refs()
MessageBody.update_forward_refs()
InlineKeyboardButton.update_forward_refs()