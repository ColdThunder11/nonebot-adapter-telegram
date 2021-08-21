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
from nonebot.drivers import Driver, HTTPConnection, HTTPResponse
#from nonebot.exception import RequestDenied

from .utils import log
from .config import Config as TelegramConfig
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed
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

    def __init__(self, self_id: str, request: HTTPConnection, **kwargs):

        super().__init__(self_id, request)

    @property
    def type(self) -> str:
        """
        - 返回: ``"telegram"``
        """
        return "telegram"

    @classmethod
    def register(cls, driver: "Driver", config: "Config", **kwargs):
        super().register(driver, config)
        cls.telegram_config = TelegramConfig(**config.dict())
        resp = httpx.post(url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/deleteWebhook")
        print(resp.json())
        resp = httpx.post(url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/setWebhook",
        json={
            "url": f"{cls.telegram_config.webhook_addr}/{cls.telegram_config.bot_token}/",
            "allowed_updates": ["message","callback_query"]
        })
        print(resp.json())
        resp = httpx.post(url=f"{cls.telegram_config.telegram_bot_api_server_addr}/bot{cls.telegram_config.bot_token}/getMe")
        cls.bot_name = resp.json()["result"]["username"]
        print("telegarm init success")

    @classmethod
    @overrides(BaseBot)
    async def check_permission(cls, driver: "Driver", request: HTTPConnection) -> Tuple[Optional[str], Optional[HTTPResponse]]:
        return cls.bot_name, None

    @overrides(BaseBot) 
    async def handle_message(self, message: bytes):
        if not message:
            return
        message_dict = json.loads(message) 
        print(message_dict)
        try:
            if "callback_query" in message_dict:
                if message_dict["callback_query"]["from"]["is_bot"]:
                    return
                event = CallbackQueryEvent.parse_obj(message_dict)
            elif "message" in message_dict:
                if message_dict["message"]["from"]["is_bot"]:
                    return
                message_dict["user_id"] = message_dict["message"]["from"]["id"]
                message_dict["group_id"] = message_dict["message"]["chat"]["id"]
                if message_dict["message"]["chat"]["type"] == "private":
                    event = PrivateMessageEvent.parse_obj(message_dict)
                elif "group" in message_dict["message"]["chat"]["type"]:
                    if "new_chat_members" in message_dict["message"]:
                        event = NewChatMembersEvent.parse_obj(message_dict)
                    elif "left_chat_member" in message_dict["message"]:
                        event = LeafChatMemberEvent.parse_obj(message_dict)
                    elif "new_chat_title" in message_dict["message"]:
                        event = NewChatTitleEvent.parse_obj(message_dict)
                    elif "voice_chat_started" in message_dict["message"]:
                        event = VoiceChatStartedEvent.parse_obj(message_dict)
                    elif "voice_chat_ended" in message_dict["message"]:
                        event = VoiceChatEndedEvent.parse_obj(message_dict)
                    else:
                        event = GroupMessageEvent.parse_obj(message_dict)
            else:
                return
                #event = MessageEvent.parse_obj(message)
            self._pre_process_event(event)
        except Exception as e:
            log("ERROR", "Event Parser Error", e)
            return
        try:
            await handle_event(self, event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
            )
        #run test
        return

    @overrides(BaseBot)
    async def _call_api(self,
                        api: str,
                        **data) -> Any:
        #if self.connection_type != "http":
        #    log("ERROR", "Only support http connection.")
        #    return
        # 将方法名称改为驼峰式 from nonebot/adapter-telegram
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )
        log("DEBUG", f"Calling API <y>{api}</y>")
        #print(data)
        headers = {}
        data: dict = data.get("data", None)
        if not data:
            raise ValueError("data not found")
        try:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(f"{self.telegram_config.telegram_bot_api_server_addr}/bot{self.telegram_config.bot_token}/{api}",
                                             json=data,
                                             timeout=self.config.api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        print(result)
                        raise ActionFailed()
                    #print(result["result"])
                    return result["result"]
            raise NetworkError(f"HTTP request received unexpected "
                               f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

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
        msg: Message = message if isinstance(message, Message) else Message(message)
        #process Message
        await self._process_send_message(event, msg, at_sender,reply_message)

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        await self.call_api("deleteMessage",data ={"chat_id":chat_id,"message_id":message_id})

    async def edit_message_text(self,chat_id:Union["int","str"],message_id:int,text: str,reply_markup:List):
        await self.call_api("editMessageText",data ={"chat_id":chat_id,"message_id":message_id,"text":text,"reply_markup":{"inline_keyboard":reply_markup}})

    async def call_multipart_form_data_api(self, api:str, file: dict, data: dict):
        log("DEBUG", f"Calling API <y>{api}</y>")
        print(data)
        for key in data:
            if isinstance(data[key],int) or isinstance(data[key],float) :
                data[key] = str(data[key])
            elif not isinstance(data[key],str):
                data[key] = json.dumps(data[key])
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.telegram_config.telegram_bot_api_server_addr}/bot{self.telegram_config.bot_token}/{api}",
                                             files=file,
                                             data=data,
                                             timeout=self.config.api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                print(result)
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        raise ActionFailed()
                    print(result["result"])
                    return result["result"]
            print(result)
            raise NetworkError(f"HTTP request received unexpected "
                               f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    #获取到的下载链接有效期一小时，应当在获取后立即下载
    async def get_file_download_link(self, file: Union[str, PhotoSizeItem, List[PhotoSizeItem], DocumentMessage]) -> str:
        print(self)
        if isinstance(file, PhotoSizeItem) or isinstance(file, DocumentMessage):
            file_id = file.file_id
        elif isinstance(file, List):
            if isinstance(file[-1],PhotoSizeItem):
                file_id = file[-1].file_id
        elif isinstance(file, str):
            file_id = file
        result = await self.call_api("getFile", data = {"file_id": file_id})
        return f"{self.telegram_config.telegram_bot_api_server_addr}/file/bot{self.telegram_config.bot_token}/{result['file_path']}"
    
    async def answer_callback_query(self, event: CallbackQueryEvent) -> None:
        await self.call_api("answerCallbackQuery",data ={"callback_query_id": event.callback_query.id})

    async def delete_callback_query_orig_message(self, event: CallbackQueryEvent) -> None:
        await self.delete_message(event.callback_query.message.chat.id,event.callback_query.message.message_id)

    async def donload_file(self, photo: Union[str, PhotoSizeItem, List[PhotoSizeItem], DocumentMessage]) -> Tuple[str, bytes] :
        download_link = await self.get_file_download_link(photo)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(download_link, timeout=self.config.api_timeout)
                i = response.aiter_bytes()
                content_list = []
                async for content_bytes in response.aiter_bytes():
                    content_list.append(content_bytes)
                return (path.basename(download_link) , b''.join(content_list))
        except httpx.InvalidURL:
            raise NetworkError("File url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")
    
    def _pre_process_event(self, event:MessageEvent):
        if isinstance(event, GroupMessageEvent):
            if event.message.text:
                if f"@{self.bot_name}" in event.message.text:
                    event.message.text = event.message.text.replace(f"@{self.bot_name}","").strip()
                    event.to_me = True
                    print(f"event.message.text:{event.message.text}")
    
    def _process_at(self,data:dict,at_user:MessageUser):
        if "text" in data:
            if at_user.username:
                data["text"] = f"@{at_user.username} " + data["text"]
            else:# some people may not have username
                data["text"] = f"{at_user.first_name} " + data["text"]#没测试
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
            else:# some people may not have username
                data["caption"] = f"{at_user.first_name} " + data["caption"]#没测试
                data["caption_entities"] = []
                data["caption_entities"].append({
                    "type": "text_mention",
                    "offset": 0,
                    "length": len(at_user.first_name),
                    "user": at_user.dict()
                })

    async def _process_send_message(self, event:MessageEvent, message: Message, at_sender: bool = False, reply_message: bool = False):
        ms_list: List[MessageSegment] = []
        core_ms: MessageSegment = None
        media_message_count: int = 0
        media_message_list: List[MessageSegment] = []
        inlineKeyboardMarkupArray = None
        media_tpye = ["photo","audio","document","video","animation","voice","video_note"]
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
                elif ms.type == "text" :
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
        if media_message_count > 1:
            #send as media group 咕咕咕
            data["chat_id"] = str(chat_id)
            data["media"] = []
            if reply_message:
                if event.message:
                    data["reply_to_message_id"] = event.message.message_id
                elif event.callback_query.message.reply_to_message:
                    data["reply_to_message_id"] = event.callback_query.message.reply_to_message["message_id"]
            files = {}
            for ms in media_message_list:
                inputMediaPhoto: dict = {"type": "photo"}
                if "caption" in ms.data:
                    inputMediaPhoto["caption"] = ms.data["caption"]
                if ms.data["photo"].startswith("file:///"):
                    if os.name == "nt":
                        file_path: str = core_ms.data[core_ms.type].replace("file:///","")
                    else:
                        file_path: str = core_ms.data[core_ms.type].replace("file://","")
                    file_name = path.basename(file_path)
                    inputMediaPhoto["media"] = f"attach://{file_name}"
                    files[file_name] = open(file_path,"rb")
                else:
                    inputMediaPhoto["media"] = ms.data["photo"]
                data["media"].append(inputMediaPhoto)
            if len(files.keys()) > 0:
                await self.call_multipart_form_data_api("sendMediaGroup",files,data)
            else:
                await self.call_api("sendMediaGroup",data = data)
            return
        #print(core_ms)
        data.update(core_ms.data)
        if "thumb" in data:
            if data["thumb"].startswith("file:///"):
                file_path: str = data["thumb"].replace("file:///","")
                file_name = path.basename(file_path)
                data["thumb"] = f"attach://{file_name}"
                files[file_name] = open(file_path,"rb")
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
            if at_sender and isinstance(event,GroupMessageEvent):
                self._process_at(data,event.message.from_)
            await self.call_api("sendMessage", data=data)
            return
        if core_ms.type in media_tpye:
            data["chat_id"] = str(chat_id)
            if "caption" in core_ms.data:
                if at_sender and isinstance(event,GroupMessageEvent):
                    self._process_at(data,event.message.from_)
            if core_ms.data[core_ms.type].startswith("file:///"):
                del data[core_ms.type]
                if os.name == "nt":
                    file_path: str = core_ms.data[core_ms.type].replace("file:///","")
                else:
                    file_path: str = core_ms.data[core_ms.type].replace("file://","")
                files[core_ms.type] = open(file_path,"rb")
            elif core_ms.data[core_ms.type].startswith("base64://"):
                del data[core_ms.type]
                file_data: str = core_ms.data[core_ms.type].replace("base64://","")
                bio = BytesIO(base64.b64decode(file_data))
                if "file_name" in core_ms.data:
                    files[core_ms.type] = (core_ms.data["file_name"], bio)
                else:
                    files[core_ms.type] = bio
            if len(files.keys()) > 0:
                await self.call_multipart_form_data_api(f"send{core_ms.type[0].upper()+core_ms.type[1:]}",files,data)
            else:
                await self.call_api(f"send{core_ms.type[0].upper()+core_ms.type[1:]}", data=data)
            return
