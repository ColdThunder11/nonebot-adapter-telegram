import asyncio
import aiocache
import redis
from redis import asyncio as aioredis
from redis.asyncio import Redis
from .utils import log

from aiocache import Cache


class TelegramCache:

    def __init__(self) -> None:
        self.session_message_cache = aiocache.Cache(Cache.MEMORY)
        self.download_link_cache = aiocache.Cache(Cache.MEMORY)

    async def get_session_last_message_id(self, session: str):
        return await self.session_message_cache.get(session)

    async def get_session_last_message_id(self, session: str, message_id: str):
        return await self.session_message_cache.set(session, message_id, ttl=600)

    async def get_media_downloadlink(self, file_id: str):
        return await self.download_link_cache.get(file_id)

    async def set_media_downloadlink(self, file_id: str, download_link: str):
        return await self.download_link_cache.set(file_id, download_link, ttl=3540)


class TelegramUserNameIdCache:

    instance: "TelegramUserNameIdCache"

    @staticmethod
    def get_inst() -> "TelegramUserNameIdCache":
        return TelegramUserNameIdCache.instance

    def __init__(self) -> None:
        self.redis: Redis = None
        self.redis_sync = None
        self.redis_on = False
        pass

    async def init(self, redis_db: int) -> bool:
        try:
            self.redis_sync = redis.from_url("redis://localhost",  db=redis_db)
            self.redis = await aioredis.from_url("redis://localhost",  db=redis_db)
            self.redis_on = True
            TelegramUserNameIdCache.instance = self
            log("INFO", f"Redis init success!")
            return True
        except:
            log("WARNING", f"Redis init failed, some function may not work like username to user_id")
            return False

    async def flush_cache(self):
        if self.redis_on:
            await self.redis.flushdb()

    async def update_cache(self, username: str, user_id: int):
        if self.redis_on:
            await self.redis.set(f"uname|{username}", user_id)

    def get_user_id(self, username: str) -> int:
        if self.redis_on:
            user_id = self.redis_sync.get(f"uname|{username}")
            if not user_id:
                return None
            return user_id if isinstance(user_id, int) else int(user_id)
        else:
            return None
