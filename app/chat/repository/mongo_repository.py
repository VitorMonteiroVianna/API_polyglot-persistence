from datetime import datetime, timezone
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.chat.repository.base import ChatRepository
from app.chat.messages.user_message import UserMessage
from app.chat.messages.genai_message import GenaiMessage


class MongoChatRepository(ChatRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        self._conversations = database["chat_conversations"]
        self._messages = database["chat_messages"]

    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        doc = {
            "user_id": user_id,
            "title": title or "Nova conversa",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = await self._conversations.insert_one(doc)
        return str(result.inserted_id)

    async def append_user_message(self, message: UserMessage) -> None:
        await self._messages.insert_one({**message.as_dict(), "role": "user"})

    async def append_genai_message(self, message: GenaiMessage) -> None:
        await self._messages.insert_one({**message.as_dict(), "role": "assistant"})

    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        cursor = self._messages.find(
            {"user_id": user_id, "conversation_id": conversation_id}
        ).sort("created_at", 1)
        return [doc async for doc in cursor]

    async def list_conversations(self, user_id: str) -> List[dict]:
        cursor = self._conversations.find({"user_id": user_id}).sort("created_at", -1)
        return [doc async for doc in cursor]