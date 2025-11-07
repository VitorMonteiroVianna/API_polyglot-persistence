from datetime import datetime
from typing import Any, List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.chat.messages.genai_message import GenaiMessage
from app.chat.messages.user_message import UserMessage
from app.chat.repository.base import ChatRepository


class MongoChatRepository(ChatRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        self._conversations = database["chat_conversations"]

    async def create_conversation(self, user_id: str, title: str | None = None) -> dict:
        conversation_id = ObjectId()
        doc = {
            "_id": str(conversation_id),
            "user_id": user_id,
            "title": title or "Nova conversa",
            "messages": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        await self._conversations.insert_one(doc)
        return doc

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[dict]:
        return await self._conversations.find_one(
            {"_id": conversation_id, "user_id": user_id}
        )

    async def list_conversations(self, user_id: str) -> List[dict]:
        cursor = self._conversations.find(
            {"user_id": user_id},
            {"messages": 0},
        ).sort("updated_at", -1)
        return [doc async for doc in cursor]

    async def save_conversation(self, conversation: dict) -> Any:
        conversation["updated_at"] = datetime.utcnow()
        result = await self._conversations.update_one(
            {"_id": conversation["_id"], "user_id": conversation["user_id"]},
            {"$set": conversation},
            upsert=True,
        )
        return result

    async def append_user_message(self, message: UserMessage) -> None:
        doc = message.as_dict()
        doc["role"] = "user"
        await self._conversations.update_one(
            {"_id": doc["conversation_id"], "user_id": doc["user_id"]},
            {
                "$setOnInsert": {
                    "title": "Nova conversa",
                    "created_at": doc["created_at"],
                    "messages": [],
                },
                "$push": {"messages": doc},
                "$set": {"updated_at": datetime.utcnow()},
            },
            upsert=True,
        )

    async def append_genai_message(self, message: GenaiMessage) -> None:
        doc = message.as_dict()
        doc["role"] = "assistant"
        await self._conversations.update_one(
            {"_id": doc["conversation_id"], "user_id": doc["user_id"]},
            {
                "$push": {"messages": doc},
                "$set": {"updated_at": datetime.utcnow()},
            },
        )

    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        conversation = await self._conversations.find_one(
            {"_id": conversation_id, "user_id": user_id},
            {"messages": 1, "_id": 0},
        )
        return conversation.get("messages", []) if conversation else []