import json
import urllib.parse
import asyncio
import os
from os import path
from io import BytesIO
import base64

from datetime import datetime
import time
from typing import Any, List, Union, Optional, Tuple, TYPE_CHECKING

import httpx
from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.drivers import Driver
#from nonebot.exception import RequestDenied

from .utils import log
from .config import Config as TelegramConfig
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed, MessageNotSupport
from .event import CallbackQueryEvent, Event, GroupMessageEvent, MessageEvent, NewChatMembersEvent, PrivateMessageEvent, LeafChatMemberEvent, NewChatTitleEvent, DeleteChatPhotoEvent, VoiceChatEndedEvent, VoiceChatStartedEvent

from .models import *

if TYPE_CHECKING:
    from nonebot.config import Config
    from nonebot.drivers import Driver


class Bot(BaseBot):
    """
    telegram 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """
    telegram_config: TelegramConfig
    bot_name: str
    self_id: str

    @classmethod
    def register(cls, driver: "Driver", config: "Config", **kwargs):
        super().register(driver, config)
        cls.telegram_config = TelegramConfig(**config.dict())
        resp = httpx.post(
            url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/deleteWebhook")
        log("info", resp.json())
        resp = httpx.post(url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/setWebhook",
                          json={
                              "url": f"{cls.telegram_config.webhook_addr}/{cls.telegram_config.bot_token}/",
                              "allowed_updates": ["message", "callback_query"]
                          })
        log("info", resp.json())
        resp = httpx.post(
            url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/getMe")
        cls.bot_name = resp.json()["result"]["username"]
        cls.self_id = cls.bot_name
        log("info", "telegarm init success")
        # driver._bot_connect(cls)
        #driver._clients[cls.self_id] = cls

    @overrides(BaseBot)
    async def call_api(self,
                       api: str,
                       **data) -> Any:
        """
        :说明:

          调用 telegram 协议 API

        :参数:

          * ``api: str``: API 名称
          * ``**data: Any``: API 参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        return await super().call_api(api, **data)

    @overrides(BaseBot)
    async def send(self,
                   event: MessageEvent,
                   message: Union[str, "Message", "MessageSegment"],
                   at_sender: bool = False,
                   reply_message: bool = False,
                   **kwargs) -> Any:
        """
        :说明:

          根据 ``event``  向触发事件的主体发送消息。

        :参数:

          * ``event: Event``: Event 对象
          * ``message: Union[str, Message, MessageSegment]``: 要发送的消息
          * ``at_sender: bool``: 是否 @ 事件主体 对隐藏了username的人会发生错误，我也不知道怎么@
          * ``reply_message``: 是否回复原消息 应尽量使用reply而不是at
          * ``**kwargs``: 覆盖默认参数

        :返回:

          - ``Any``: API 调用返回数据

        :异常:

          - ``ValueError``: 缺少 ``user_id``, ``group_id``
          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        msg: Message = message if isinstance(
            message, Message) else Message(message)
        # process Message
        await self._process_send_message(event, msg, at_sender, reply_message)

    async def call_multipart_form_data_api(self, api: str, file: dict, data: dict):
        return await self.adapter._call_multipart_form_data_api(api, file, data)

    # 获取到的下载链接有效期一小时，应当在获取后立即下载
    async def get_file_download_link(self, file: Union[str, PhotoSize, List[PhotoSize], Document]) -> str:
        if isinstance(file, PhotoSize) or isinstance(file, Document):
            file_id = file.file_id
        elif isinstance(file, List):
            if isinstance(file[-1], PhotoSize):
                file_id = file[-1].file_id
        elif isinstance(file, str):
            file_id = file
        if link := await self.adapter.cache.get_media_downloadlink(file_id):
            return link
        result = await self.call_api("getFile", file_id=file_id)
        if not result['file_path']:
            raise ActionFailed(403,"getFile not return correctly")
        if result['file_path'].startswith("/"):  # local bot api
            await self.adapter.cache.set_media_downloadlink(
                file_id, result['file_path'])
            return result['file_path']
        else:
            await self.adapter.cache.set_media_downloadlink(
                file_id, f"{self.adapter.telegram_config.telegram_bot_api_server_addr}/file/bot{self.adapter.telegram_config.bot_token}/{result['file_path']}")
            return f"{self.adapter.telegram_config.telegram_bot_api_server_addr}/file/bot{self.adapter.telegram_config.bot_token}/{result['file_path']}"

    async def answer_callback_query(self, event: CallbackQueryEvent) -> None:
        await self.call_api("answerCallbackQuery", callback_query_id=event.callback_query.id)

    async def delete_callback_query_orig_message(self, event: CallbackQueryEvent) -> None:
        await self.delete_message(event.callback_query.message.chat.id, event.callback_query.message.message_id)

    async def download_file(self, photo: Union[str, PhotoSize, List[PhotoSize], Document]) -> Tuple[str, bytes]:
        download_link = await self.get_file_download_link(photo)
        if download_link.startswith("/"):
            with open(download_link, "rb") as fp:
                return (path.basename(download_link), fp.read())
        else:
            try:
                async with httpx.AsyncClient(proxies=self.adapter.telegram_config.telegram_bot_api_proxy) as client:
                    response = await client.get(download_link, timeout=self.config.api_timeout)
                    i = response.aiter_bytes()
                    content_list = []
                    async for content_bytes in response.aiter_bytes():
                        content_list.append(content_bytes)
                    return (path.basename(download_link), b''.join(content_list))
            except httpx.InvalidURL:
                raise NetworkError("File url invalid")
            except httpx.HTTPError:
                raise NetworkError("HTTP request failed")

    def _process_at(self, data: dict, at_user: User):
        if "text" in data:
            if at_user.username:
                data["text"] = f"@{at_user.username} " + data["text"]
            else:  # some people may not have username
                data["text"] = f"{at_user.first_name} " + data["text"]  # 没测试
                data["entities"] = []
                data["entities"].append({
                    "type": "text_mention",
                    "offset": 0,
                    "length": len(at_user.first_name),
                    "user": at_user.dict()
                })
        elif "caption" in data:
            if at_user.username:
                data["caption"] = f"@{at_user.username} " + data["caption"]
            else:  # some people may not have username
                data["caption"] = f"{at_user.first_name} " + \
                    data["caption"]  # 没测试
                data["caption_entities"] = []
                data["caption_entities"].append({
                    "type": "text_mention",
                    "offset": 0,
                    "length": len(at_user.first_name),
                    "user": at_user.dict()
                })

    async def _process_send_message(self, event: MessageEvent, message: Message, at_sender: bool = False, reply_message: bool = False):
        ms_list: List[MessageSegment] = []
        core_ms: MessageSegment = None
        media_message_count: int = 0
        media_message_list: List[MessageSegment] = []
        inlineKeyboardMarkupArray = None
        media_tpye = ["photo", "audio", "document",
                      "video", "animation", "voice", "video_note"]
        if event.message:
            chat_id = event.message.chat.id
        elif event.callback_query:
            chat_id = event.callback_query.message.chat.id
        for ms in message:
            if ms.type == "photo":
                media_message_count += 1
                media_message_list.append(ms)
            ms_list.append(ms)
        if len(ms_list) > 1:
            for ms in ms_list:
                if ms.type in media_tpye:
                    core_ms = ms
                elif ms.type == "text":
                    if core_ms != None:
                        if core_ms.type in media_tpye:
                            if not "caption" in core_ms.data:
                                core_ms.data["caption"] = ms.data["text"]
                            else:
                                core_ms.data["caption"] += ms.data["text"]
                    else:
                        core_ms = ms
                elif ms.type == "markup":
                    inlineKeyboardMarkupArray = ms.data["inline_keyboard"]
        else:
            core_ms = ms_list[0]
        data = {}
        files = {}
        if media_message_count > 1: #fix need
            # send as media group 咕咕咕
            data["chat_id"] = str(chat_id)
            data["media"] = []
            if reply_message:
                if event.message:
                    data["reply_to_message_id"] = event.message.message_id
                elif event.callback_query.message.reply_to_message:
                    data["reply_to_message_id"] = event.callback_query.message.reply_to_message["message_id"]
            files = {}
            file_attach_num_name = 0
            for ms in media_message_list: #fix need
                file_attach_num_name += 1
                if ms.type != "photo":
                    raise MessageNotSupport()
                inputMediaPhoto: dict = {"type": "photo"}
                if "caption" in ms.data:
                    inputMediaPhoto["caption"] = ms.data["caption"]
                if isinstance(ms.data["photo"],str):
                    if ms.data["photo"].startswith("file:///"):
                        file_path: str = core_ms.data[core_ms.type].replace(
                            "file:///", "")
                        file_name = path.basename(file_path)
                        inputMediaPhoto["media"] = f"attach://{file_name}"
                        files[file_name] = open(file_path, "rb")
                    elif ms.data["photo"].startswith("base64://"):
                        file_data: str = core_ms.data[core_ms.type].replace("base64://", "")
                        inputMediaPhoto["media"] = f"attach://{file_attach_num_name}"
                        files[file_attach_num_name] = BytesIO(base64.b64decode(file_data))
                    else:
                        inputMediaPhoto["media"] = ms.data["photo"]
                elif isinstance(core_ms.data[core_ms.type],bytes):
                    inputMediaPhoto["media"] = f"attach://{file_attach_num_name}"
                    files[file_attach_num_name] = BytesIO(core_ms.data[core_ms.type])
                elif isinstance(core_ms.data[core_ms.type],BytesIO):
                    inputMediaPhoto["media"] = f"attach://{file_attach_num_name}"
                    files[file_attach_num_name] = core_ms.data[core_ms.type]
                else:
                    raise MessageNotSupport()
                data["media"].append(inputMediaPhoto)
            if len(files.keys()) > 0:
                await self.call_multipart_form_data_api("sendMediaGroup", files, data)
            else:
                await self.call_api("sendMediaGroup", **data)
            return
        # print(core_ms)
        data.update(core_ms.data)
        if "thumb" in data:
            if data["thumb"].startswith("file:///"):
                file_path: str = data["thumb"].replace("file:///", "")
                file_name = path.basename(file_path)
                data["thumb"] = f"attach://{file_name}"
                files[file_name] = open(file_path, "rb")
        if core_ms.type == "text" or core_ms.type in media_tpye:
            if reply_message:
                if event.message:
                    data["reply_to_message_id"] = event.message.message_id
                elif event.callback_query.message.reply_to_message:
                    data["reply_to_message_id"] = event.callback_query.message.reply_to_message["message_id"]
            if inlineKeyboardMarkupArray:
                data["reply_markup"] = {}
                data["reply_markup"]["inline_keyboard"] = inlineKeyboardMarkupArray
        if core_ms.type == "text":
            data["chat_id"] = chat_id
            if at_sender and isinstance(event, GroupMessageEvent):
                self._process_at(data, event.message.from_)
            await self.call_api("sendMessage", **data)
            return
        if core_ms.type in media_tpye:
            data["chat_id"] = str(chat_id)
            if "caption" in core_ms.data:
                if at_sender and isinstance(event, GroupMessageEvent):
                    self._process_at(data, event.message.from_)
            if isinstance(core_ms.data[core_ms.type],bytes):
                bio = BytesIO(core_ms.data[core_ms.type])
                if "file_name" in core_ms.data:
                    files[core_ms.type] = (core_ms.data["file_name"], bio)
                else:
                    files[core_ms.type] = bio
                del data[core_ms.type]
            elif isinstance(core_ms.data[core_ms.type],BytesIO):
                bio = core_ms.data[core_ms.type]
                if "file_name" in core_ms.data:
                    files[core_ms.type] = (core_ms.data["file_name"], bio)
                else:
                    files[core_ms.type] = bio
                del data[core_ms.type]
            elif isinstance(core_ms.data[core_ms.type],str):
                if core_ms.data[core_ms.type].startswith("file:///"):
                    del data[core_ms.type]
                    file_path: str = core_ms.data[core_ms.type].replace(
                        "file:///", "")
                    files[core_ms.type] = open(file_path, "rb")
                elif core_ms.data[core_ms.type].startswith("base64://"):
                    del data[core_ms.type]
                    file_data: str = core_ms.data[core_ms.type].replace(
                        "base64://", "")
                    bio = BytesIO(base64.b64decode(file_data))
                    if "file_name" in core_ms.data:
                        files[core_ms.type] = (core_ms.data["file_name"], bio)
                    else:
                        files[core_ms.type] = bio
            else:
                raise MessageNotSupport()
            if len(files.keys()) > 0:
                await self.call_multipart_form_data_api(f"send{core_ms.type[0].upper()+core_ms.type[1:]}", files, data)
            else:
                await self.call_api(f"send{core_ms.type[0].upper()+core_ms.type[1:]}", **data)
            return
