from datetime import datetime
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.chat.interfaces.repository.i_mongo_chat_repository import IMongoChatRepository
from app.chat.messages.user_message import UserMessage
from app.chat.messages.genai_message import GenaiMessage
from app.core.config import settings


class MongoChatRepository(IMongoChatRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        self.__conversations = database[settings.MONGO_CONVERSATIONS_COLLECTION]
        self.__messages = database[settings.MONGO_MESSAGES_COLLECTION]

    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        doc = {
            "user_id": user_id,
            "title": title or "Nova conversa",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        result = await self.__conversations.insert_one(doc)
        return str(result.inserted_id)

    async def append_user_message(self, message: UserMessage) -> None:
        await self.__messages.insert_one({**message.as_dict(), "role": "user"})

    async def append_genai_message(self, message: GenaiMessage) -> None:
        await self.__messages.insert_one({**message.as_dict(), "role": "assistant"})

    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        cursor = self.__messages.find(
            {"user_id": user_id, "conversation_id": conversation_id}
        ).sort("created_at", 1)
        return [doc async for doc in cursor]

    async def list_conversations(self, user_id: str) -> List[dict]:
        cursor = self.__conversations.find({"user_id": user_id}).sort("updated_at", -1)
        conversations: List[dict] = []
        async for doc in cursor:
            cleaned = self.__strip_id(doc)
            if cleaned is not None:
                conversations.append(cleaned)
        return conversations

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[dict]:
        doc = await self.__conversations.find_one(
            {"_id": conversation_id, "user_id": user_id}
        )
        return self.__strip_id(doc)

    async def save_conversation(self, conversation: dict) -> None:
        conversation_id = conversation.get("conversation_id")
        user_id = conversation.get("user_id")
        if not conversation_id or not user_id:
            raise ValueError("conversation must include 'conversation_id' and 'user_id'")

        payload = self.__serialize(conversation)
        payload["_id"] = conversation_id

        await self.__conversations.update_one(
            {"_id": conversation_id, "user_id": user_id},
            {"$set": payload},
            upsert=True,
        )

    def __serialize(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: self.__serialize(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self.__serialize(item) for item in value]
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def __jsonify(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: self.__jsonify(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self.__jsonify(item) for item in value]
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def __strip_id(self, doc: Optional[dict]) -> Optional[dict]:
        if not doc:
            return doc
        cleaned = dict(doc)
        cleaned.pop("_id", None)
        return cleaned
