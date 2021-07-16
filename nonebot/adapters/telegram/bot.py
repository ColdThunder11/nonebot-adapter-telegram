import json
import urllib.parse
import asyncio
from os import path

from datetime import datetime
import time
from typing import Any, List, Union, Optional, TYPE_CHECKING

import httpx
from nonebot.log import logger
from nonebot.typing import overrides
from nonebot.message import handle_event
from nonebot.adapters import Bot as BaseBot
from nonebot.exception import RequestDenied

from .utils import log
from .config import Config as TelegramConfig
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed, SessionExpired
from .event import CallbackQueryEvent, DocumentMessage, Event, GroupMessageEvent, MessageEvent, PhotoSizeItem, PrivateMessageEvent

if TYPE_CHECKING:
    from nonebot.config import Config
    from nonebot.drivers import Driver


class Bot(BaseBot):
    """
    telegram 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`_ 。
    """
    telegram_config: TelegramConfig
    bot_name: str

    def __init__(self, connection_type: str, self_id: str, **kwargs):

        super().__init__(connection_type, self_id, **kwargs)

    @property
    def type(self) -> str:
        """
        - 返回: ``"telegram"``
        """
        return "telegram"

    @classmethod
    def register(cls, driver: "Driver", config: "Config"):
        super().register(driver, config)
        cls.telegram_config = TelegramConfig(**config.dict())
        
        resp = httpx.post(url=f"https://api.telegram.org/bot{cls.telegram_config.bot_token}/deleteWebhook")
        print(resp.json())
        resp = httpx.post(url=f"https://api.telegram.org/bot{cls.telegram_config.bot_token}/setWebhook",
        json={
            "url": f"https://{cls.telegram_config.webhook_host}/{cls.telegram_config.bot_token}/",
            "allowed_updates": ["message","callback_query"]
        })
        print(resp.json())
        resp = httpx.post(url=f"https://api.telegram.org/bot{cls.telegram_config.bot_token}/getMe")
        cls.bot_name = resp.json()["result"]["username"]
        print("telegarm init success")

    @classmethod
    @overrides(BaseBot)
    async def check_permission(cls, driver: "Driver", connection_type: str,
                               headers: dict, body: Optional[bytes]) -> str:
        return cls.bot_name

    @overrides(BaseBot) 
    async def handle_message(self, message: dict):
        if not message:
            return
        print
        try:
            if "callback_query" in message:
                if message["callback_query"]["from"]["is_bot"]:
                    return
                event = CallbackQueryEvent.parse_obj(message)
            
            elif "message" in message:
                if message["message"]["from"]["is_bot"]:
                    return
                if message["message"]["chat"]["type"] == "private":
                    event = PrivateMessageEvent.parse_obj(message)
                elif "group" in message["message"]["chat"]["type"]:
                    event = GroupMessageEvent.parse_obj(message)
            else:
                return
                #event = MessageEvent.parse_obj(message)
            self.pre_process_event(event)
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
        if self.connection_type != "http":
            log("ERROR", "Only support http connection.")
            return

        log("DEBUG", f"Calling API <y>{api}</y>")
        print(data)
        headers = {}
        data: dict = data.get("data", None)
        if not data:
            raise ValueError("data not found")
        try:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(f"https://api.telegram.org/bot{self.telegram_config.bot_token}/{api}",
                                             json=data,
                                             timeout=self.config.api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        print(result)
                        raise ActionFailed()
                    print(result["result"])
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
        await self.process_send_message(event, msg, at_sender,reply_message)

    async def delete_message(self, chat_id: int, message_id: int) -> None:
        await self.call_api("deleteMessage",data ={"chat_id":chat_id,"message_id":message_id})

    async def edit_message_text(self,chat_id:Union["int","str"],message_id:int,text: str,reply_markup:List):
        await self.call_api("editMessageText",data ={"chat_id":chat_id,"message_id":message_id,"text":text,"reply_markup":{"inline_keyboard":reply_markup}})

    async def call_multipart_form_data_api(self, api:str, file: dict, data: dict):
        log("DEBUG", f"Calling API <y>{api}</y>")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"https://api.telegram.org/bot{self.telegram_config.bot_token}/{api}",
                                             files=file,
                                             data=data,
                                             timeout=self.config.api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        raise ActionFailed()
                    print(result["result"])
                    return result["result"]
            print(result = response.json())
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
        return f"https://api.telegram.org/file/bot{self.telegram_config.bot_token}/{result['file_path']}"
    
    async def answer_callback_query(self, event: CallbackQueryEvent) -> None:
        await self.call_api("answerCallbackQuery",data ={"callback_query_id": event.callback_query.id})

    async def delete_orig_message(self, event: CallbackQueryEvent) -> None:
        await self.delete_message(event.callback_query.message.chat.id,event.callback_query.message.message_id)

    async def donload_photo(self, photo: Union[PhotoSizeItem, List[PhotoSizeItem]]) -> bytes:
        download_link = self.get_file_download_link(photo)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(download_link, timeout=self.config.api_timeout)
                return response.content
        except httpx.InvalidURL:
            raise NetworkError("File url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")
    
    def pre_process_event(self, event:MessageEvent):
        if isinstance(event, GroupMessageEvent):
            print("pre_process group message")
            if event.message.text:
                if f"@{self.bot_name}" in event.message.text:
                    event.message.text = event.message.text.replace(f"@{self.bot_name}","").strip()
                    event.to_me = True
                    print(f"event.message.text:{event.message.text}")
    
    async def process_send_message(self, event:MessageEvent, message: Message, at_sender: bool = False, reply_message: bool = False):
        ms_list: List[MessageSegment] = []
        core_ms: MessageSegment = None
        media_message_count: int = 0
        inlineKeyboardMarkupArray = None
        if event.message:
            chat_id = event.message.chat.id
        elif event.callback_query:
            chat_id = event.callback_query.message.chat.id
        for ms in message:
            if ms.type == "photo":
                media_message_count += 1
            ms_list.append(ms)
        if media_message_count > 1:
            #send as media group
            return
            pass
        if len(ms_list) > 1:
            for ms in ms_list:
                if ms.type == "photo":
                    core_ms = ms
                elif ms.type == "text" :
                    if core_ms != None:
                        if core_ms.type == "photo":
                            if "caption" in core_ms.data:
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
        if core_ms.type == "text" or core_ms.type == "photo":
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
                if event.message.mfrom.username:
                    data["text"] = f"@{event.message.mfrom.username} {core_ms.data['text']}"# some people may not have username
                else:
                    data["text"] = f"@{event.message.mfrom.id} {core_ms.data['text']}"#可用性存疑，我猜的
            else:
                data["text"] = core_ms.data["text"]
            await self.call_api("sendMessage", data=data)
        elif core_ms.type == "photo":
            data["chat_id"] = str(chat_id)
            if "caption" in core_ms.data:
                data["caption"] = core_ms.data["caption"]
            if core_ms.data["file"].startswith("file:///"):
                file_path: str = core_ms.data["file"].lstrip("file:///")
                await self.call_multipart_form_data_api("sendPhoto",{"photo": open(file_path,"rb")},data)
            else:
                data["photo"] = core_ms.data["file"]
                await self.call_api("sendPhoto", **{"data":data})