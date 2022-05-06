from dataclasses import dataclass
import imp
import json
import asyncio
import inspect
import traceback
import httpx
import aiocache
from typing import Any, Dict, List, Type, Union, Callable, Optional, cast

from pygtrie import StringTrie
from nonebot.typing import overrides
from nonebot.log import logger
from nonebot.exception import WebSocketClosed
from nonebot.utils import DataclassEncoder, escape_tag
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    WebSocket,
    ForwardDriver,
    ReverseDriver,
    HTTPServerSetup,
    WebSocketServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter

from . import event
from .bot import Bot
from .config import Config as TelegramConfig
from .event import (
    Event,
    GroupMessageEvent,
    MessageEvent,
    NewChatMembersEvent,
    PrivateMessageEvent,
    LeafChatMemberEvent,
    NewChatTitleEvent,
    DeleteChatPhotoEvent,
    VoiceChatEndedEvent,
    VoiceChatStartedEvent,
    CallbackQueryEvent
)
from .message import Message, MessageSegment
from .exception import NetworkError, ApiNotAvailable, ActionFailed, TelegramAdapterConfigException, MessageNotAcceptable
from .utils import log
from .cache import TelegramCache

from nonebot.message import handle_event


class Adapter(BaseAdapter):

    telegram_config: TelegramConfig
    bot_name: str
    use_long_polling: bool
    cache: TelegramCache


    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        self.telegram_config: TelegramConfig = TelegramConfig(
            **self.config.dict())
        self.tasks: List["asyncio.Task"] = []
        self._check_config()
        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self._call_api(None, "deleteWebhook"))
        #self.bot_name = loop.run_until_complete(self._call_api(None, "getMe"))["username"]
        # setup route
        log("INFO", f"Current driver:{self.driver.type}")
        if "httpx" in self.driver.type:
            self.driver.on_startup(self._start_polling)
            self.driver.on_shutdown(self._stop_polling)
        elif "fastapi" in self.driver.type:
            http_setup = HTTPServerSetup(
                URL(f"/{self.telegram_config.bot_token}"), "POST", self.get_name(), self._handle_webhook
            )
            self.setup_http_server(http_setup)
            self.driver.on_startup(self._setup_webhook)
        else:
            raise TelegramAdapterConfigException("No avaliable driver type")
        #setup cache
        self.cache = TelegramCache()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        """适配器名称: `Telegram`"""
        return "Telegram"

    @overrides(BaseAdapter)
    async def _call_api(self,
                        bot: Bot,
                        api: str,
                        **data) -> Any:
        # if self.connection_type != "http":
        #    log("ERROR", "Only support http connection.")
        #    return
        # 将方法名称改为驼峰式 from nonebot/adapter-telegram
        api = api.split("_", maxsplit=1)[0] + "".join(
            s.capitalize() for s in api.split("_")[1:]
        )
        if self.use_long_polling and api == "getUpdates":
            api_timeout = self.telegram_config.telegram_long_polling_timeout
        else:
            api_timeout=self.config.api_timeout
        log("DEBUG", f"Calling API <y>{api}</y>")
        # print(data)
        headers = {"Content-Type": "application/json"}
        if not data:
            data = {}
            #raise ValueError("data not found")
        if data.get("data") != None and len(data) == 1:
            data = data.get("data")
        try:
            async with httpx.AsyncClient(headers=headers,proxies=self.telegram_config.telegram_bot_api_proxy) as client:
                response = await client.post(f"{self.telegram_config.telegram_bot_api_server_addr}/bot{self.telegram_config.bot_token}/{api}",
                                             json=data,
                                             timeout=api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        #print(result)
                        raise ActionFailed(result.get("error_code"),result.get("description"))
                    # print(result["result"])
                    return result["result"]
            raise NetworkError(f"HTTP request received unexpected "
                               f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    async def _call_multipart_form_data_api(self, api: str, file: dict, data: dict):
        log("DEBUG", f"Calling API <y>{api}</y>")
        #print(data)
        for key in data:
            if isinstance(data[key], int) or isinstance(data[key], float):
                data[key] = str(data[key])
            elif not isinstance(data[key], str):
                try:
                    data[key] = json.dumps(data[key])
                except:
                    del data[key]
        try:
            async with httpx.AsyncClient(proxies=self.telegram_config.telegram_bot_api_proxy) as client:
                response = await client.post(f"{self.telegram_config.telegram_bot_api_server_addr}/bot{self.telegram_config.bot_token}/{api}",
                                             files=file,
                                             data=data,
                                             timeout=self.config.api_timeout)
            if 200 <= response.status_code < 500:
                result = response.json()
                #print(result)
                if isinstance(result, dict):
                    if result.get("ok") != True:
                        raise ActionFailed()
                    #print(result["result"])
                    return result["result"]
            #print(result)
            raise NetworkError(f"HTTP request received unexpected "
                               f"status code: {response.status_code}")
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")
        finally:
                for file_obj in file.values():
                    try:
                        file_obj.close()
                    except:
                        pass

    def _check_config(self):
        if not self.telegram_config.bot_token:
            raise TelegramAdapterConfigException("bot token not set")
        if self.telegram_config.telegram_polling_interval == 0 and self.telegram_config.telegram_long_polling_timeout == 0:
            raise TelegramAdapterConfigException(
                "telegram_polling_interval and telegram_long_polling_timeout are both 0, please check your config")
        if self.telegram_config.telegram_polling_interval != 0 and self.telegram_config.telegram_long_polling_timeout != 0:
            raise TelegramAdapterConfigException(
                "telegram_polling_interval and telegram_long_polling_timeout are both not 0, please check your config")
        if self.telegram_config.telegram_polling_interval == 0:
            self.use_long_polling = True
        else:
            self.use_long_polling = False

    async def _setup_webhook(self):
        await self._call_api(None, "deleteWebhook")
        username = (await self._call_api(None, "getMe"))["username"]
        self.bot_name = username
        await self._call_api(None, "setWebhook", url=f"{self.telegram_config.webhook_addr}/{self.telegram_config.bot_token}/")

    async def _handle_webhook(self, request: Request) -> Response:
        data = request.content
        json_data = json.loads(data)
        event = self.json_to_event(json_data)
        try:
            await handle_event(Bot(self, self.bot_name), event)
        except Exception as e:
            logger.opt(colors=True, exception=e).error(
                f"<r><bg #f8bbd0>Failed to handle event. Raw: {json_data}</bg #f8bbd0></r>"
            )
        return Response(200)

    def _pre_process_event(self, event: MessageEvent):
        if isinstance(event, GroupMessageEvent):
            if event.message.text:
                if f"@{self.bot_name}" in event.message.text:
                    event.message.text = event.message.text.replace(
                        f"@{self.bot_name}", "").strip()
                    event.to_me = True
                    print(f"event.message.text:{event.message.text}")

    def json_to_event(self, json_data: Any) -> Optional[Event]:
        try:
            #print(json_data)
            if "callback_query" in json_data:
                if json_data["callback_query"]["from"]["is_bot"]:
                    return
                event = CallbackQueryEvent.parse_obj(json_data)
            elif "message" in json_data:
                if json_data["message"]["from"]["is_bot"]:
                    return
                json_data["user_id"] = json_data["message"]["from"]["id"]
                json_data["group_id"] = json_data["message"]["chat"]["id"]
                if json_data["message"]["chat"]["type"] == "private":
                    event = PrivateMessageEvent.parse_obj(json_data)
                elif "group" in json_data["message"]["chat"]["type"]:
                    if "new_chat_members" in json_data["message"]:
                        event = NewChatMembersEvent.parse_obj(json_data)
                    elif "left_chat_member" in json_data["message"]:
                        event = LeafChatMemberEvent.parse_obj(json_data)
                    elif "new_chat_title" in json_data["message"]:
                        event = NewChatTitleEvent.parse_obj(json_data)
                    elif "voice_chat_started" in json_data["message"]:
                        event = VoiceChatStartedEvent.parse_obj(json_data)
                    elif "voice_chat_ended" in json_data["message"]:
                        event = VoiceChatEndedEvent.parse_obj(json_data)
                    else:
                        event = GroupMessageEvent.parse_obj(json_data)
            else:
                raise MessageNotAcceptable("")
                #event = MessageEvent.parse_obj(message)
            self._pre_process_event(event)
            return event
        except Exception as e:
            log("ERROR", "Event Parser Error", e)
            raise MessageNotAcceptable("")

    async def _stop_polling(self) -> None:
        try:
            for task in self.tasks:
                if not task.done():
                    task.cancel()

            await asyncio.gather(*self.tasks, return_exceptions=True)
        except:
            pass

    async def _start_polling(self):
        async def polling_handle_event(message, bot, event):
            try:
                await handle_event(bot, event)
            except Exception as e:
                logger.opt(colors=True, exception=e).error(
                    f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
                )

        async def polling():
            await self._call_api(None, "deleteWebhook")
            username = (await self._call_api(None, "getMe"))["username"]
            self.bot_name = username
            bot = Bot(self, self.bot_name)
            log("INFO", "Reset Update...")
            await self._call_api(None, "getUpdates", offset=-1, timeout=self.telegram_config.telegram_long_polling_timeout)
            offset: int = 0
            log("INFO", "Start polling")
            while True:
                try:
                    messages = await self._call_api(None, "getUpdates", offset=offset if not offset == 0 else None, timeout=self.telegram_config.telegram_long_polling_timeout)
                    for message in messages:
                        if offset < message["update_id"] + 1:
                            offset = message["update_id"] + 1
                            #print(f"offset update to {offset}")
                        event = self.json_to_event(message)
                        try:
                            loop = asyncio.get_event_loop() 
                            loop.create_task(polling_handle_event(message, bot, event))
                        except Exception as e:
                            logger.opt(colors=True, exception=e).error(
                                f"<r><bg #f8bbd0>Failed to handle event. Raw: {message}</bg #f8bbd0></r>"
                            )
                except (KeyboardInterrupt,asyncio.exceptions.CancelledError):
                    break
                except NetworkError:
                    if not self.use_long_polling:
                        log("ERROR", "Failed to handle polling")
                        traceback.print_exc()
                except:
                        log("ERROR", "Failed to handle polling")
                        traceback.print_exc()
                if not self.use_long_polling:
                    await asyncio.sleep(self.telegram_config.telegram_polling_interval)

        log("INFO", "Setting up polling...")
        self.tasks.append(asyncio.create_task(polling()))
