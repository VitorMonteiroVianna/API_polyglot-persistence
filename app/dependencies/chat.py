from functools import lru_cache

import redis.asyncio as redis
from redis.asyncio import Redis

from app.chat.repository.base import ChatRepository
from app.chat.repository.mongo_repository import MongoChatRepository
from app.chat.repository.cached_repository import CachedChatRepository
from app.core.config import mongo_db, settings


@lru_cache
def get_redis_client() -> Redis:
    cfg = settings.redis
    return redis.Redis(
        host=cfg.host,
        port=cfg.port,
        username=cfg.username,
        password=cfg.password,
        decode_responses=cfg.decode_responses,
    )


@lru_cache
def get_mongo_repository() -> MongoChatRepository:
    return MongoChatRepository(database=mongo_db)


def get_chat_repository() -> ChatRepository:
    return CachedChatRepository(
        repository=get_mongo_repository(),
        cache=get_redis_client(),
        ttl_seconds=settings.redis.ttl_seconds,
    )