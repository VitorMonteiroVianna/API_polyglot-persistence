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
        conversation_id = payload.chat_id or await self._repository.create_conversation(
            user_id=user_id, title=getattr(payload, "title", None)
        )

        user_message = UserMessage(
            text=payload.prompt,
            genai_model=payload.genai_model,
            conversation_id=conversation_id,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
            user_id=user_id,
        )
        await self._repository.append_user_message(user_message)

        completion = await self._handler.generate_completion(user_message)
        genai_message = GenaiMessage(
            text=completion.text,
            genai_model=user_message.genai_model,
            conversation_id=conversation_id,
            user_message_id=user_message.message_id,
            genai_role=completion.role,
            genai_usage=completion.usage,
        )
        await self._repository.append_genai_message(genai_message)

        return {
            "conversation_id": conversation_id,
            "messages": [user_message.as_dict(), genai_message.as_dict()],
        }

    async def get_history(self, user_id: str, conversation_id: str) -> list[dict]:
        return await self._repository.list_messages(user_id=user_id, conversation_id=conversation_id)