from __future__ import annotations

import json
from datetime import datetime
from typing import Any, List

from bson import ObjectId
from redis.asyncio import Redis

from app.chat.messages.genai_message import GenaiMessage
from app.chat.messages.user_message import UserMessage
from app.chat.repository.base import ChatRepository


class CachedChatRepository(ChatRepository):
    """Decorates a ChatRepository adding Redis caching."""

    def __init__(
        self,
        repository: ChatRepository,
        cache: Redis,
        ttl_seconds: int = 600,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._ttl_seconds = ttl_seconds

    def __getattr__(self, name: str) -> Any:
        return getattr(self._repository, name)

    async def append_user_message(self, message: UserMessage) -> None:
        await self._repository.append_user_message(message)
        await self._refresh_cache(
            str(message.user_id),
            str(message.conversation_id),
        )

    async def append_genai_message(self, message: GenaiMessage) -> None:
        await self._repository.append_genai_message(message)
        await self._refresh_cache(
            str(message.user_id),
            str(message.conversation_id),
        )

    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        key = self._cache_key(user_id, conversation_id)
        if self._cache:
            cached = await self._cache.get(key)
            if cached:
                return json.loads(cached)

        messages = await self._repository.list_messages(user_id, conversation_id)
        await self._store_cache(key, messages)
        return messages

    async def create_conversation(self, *args, **kwargs):
        return await self._repository.create_conversation(*args, **kwargs)

    async def get_conversation(self, *args, **kwargs):
        return await self._repository.get_conversation(*args, **kwargs)

    async def list_conversations(self, *args, **kwargs):
        return await self._repository.list_conversations(*args, **kwargs)

    async def save_conversation(self, *args, **kwargs):
        result = await self._repository.save_conversation(*args, **kwargs)
        conversation = kwargs.get("conversation")
        await self._clear_related_cache(conversation)
        return result

    async def _refresh_cache(self, user_id: str, conversation_id: str) -> None:
        if not self._cache:
            return
        key = self._cache_key(user_id, conversation_id)
        messages = await self._repository.list_messages(user_id, conversation_id)
        await self._store_cache(key, messages)

    async def _store_cache(self, key: str, messages: List[dict] | None) -> None:
        if not self._cache:
            return
        if not messages:
            await self._cache.delete(key)
            return
        payload = json.dumps(messages, default=self._json_serializer)
        await self._cache.setex(key, self._ttl_seconds, payload)

    async def _clear_related_cache(self, conversation: Any) -> None:
        if not self._cache or conversation is None:
            return
        user_id = getattr(conversation, "user_id", None)
        conversation_id = getattr(conversation, "id", None)

        if isinstance(conversation, dict):
            user_id = user_id or conversation.get("user_id")
            conversation_id = conversation_id or conversation.get("_id") or conversation.get("id")

        if user_id and conversation_id:
            await self._cache.delete(self._cache_key(str(user_id), str(conversation_id)))

    @staticmethod
    def _cache_key(user_id: str, conversation_id: str) -> str:
        return f"chat:{user_id}:{conversation_id}"

    @staticmethod
    def _json_serializer(obj: Any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return str(obj)