from datetime import datetime, timezone
from typing import Optional

from app.chat.messages.user_message import UserMessage
from app.chat.messages.genai_message import GenaiMessage
from app.chat.repository import ChatRepository
from app.genai.handler import GenaiHander
from app.shared import utils


class ChatService:
    def __init__(self, repository: ChatRepository, handler: GenaiHander):
        self._repository = repository
        self._handler = handler

    async def send_message(self, user_id: str, payload) -> dict:
        conversation_id = payload.chat_id or utils.generate_hash_id()
        conversation = await self._repository.get_conversation(
            user_id=user_id, conversation_id=conversation_id
        )

        now = datetime.now(timezone.utc)
        if not conversation:
            conversation = {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "title": getattr(payload, "title", "Nova conversa"),
                "created_at": now,
                "messages": [],
            }

        user_message = UserMessage(
            text=payload.prompt,
            genai_model=payload.genai_model,
            conversation_id=conversation_id,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
            user_id=user_id,
        )
        conversation["messages"].append(user_message.as_dict())

        genai_message: GenaiMessage = self._handler.get_completions(user_message)
        conversation["messages"].append(genai_message.as_dict())

        conversation["updated_at"] = now
        await self._repository.save_conversation(conversation)

        return {
            "conversation_id": conversation_id,
            "messages": conversation["messages"],
        }

    async def get_history(self, user_id: str, conversation_id: str) -> list[dict]:
        conversation = await self._repository.get_conversation(
            user_id=user_id, conversation_id=conversation_id
        )
        if not conversation:
            return []
        return conversation.get("messages", [])