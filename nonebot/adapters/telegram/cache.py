import asyncio
import aiocache

from aiocache import Cache

class TelegramCache:

    def __init__(self) -> None:
        self.session_message_cache = aiocache.Cache(Cache.MEMORY)
        self.download_link_cache = aiocache.Cache(Cache.MEMORY)

    async def get_session_last_message_id(self, session:str):
        return await self.session_message_cache.get(session)
    
    async def get_session_last_message_id(self, session:str, message_id: str):
        return await self.session_message_cache.set(session,message_id,ttl=600)

    async def get_media_downloadlink(self, file_id:str):
        return await self.download_link_cache.get(file_id)

    async def set_media_downloadlink(self, file_id:str, download_link:str):
        return await self.download_link_cache.set(file_id,download_link,ttl=3540)