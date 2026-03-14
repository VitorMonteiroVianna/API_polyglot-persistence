from abc import ABC
from typing import List, Optional

from app.chat.messages.user_message import UserMessage
from app.chat.messages.genai_message import GenaiMessage


class IChatRepository(ABC):
    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        raise NotImplementedError()

    async def append_user_message(self, message: UserMessage) -> None:
        raise NotImplementedError()

    async def append_genai_message(self, message: GenaiMessage) -> None:
        raise NotImplementedError()

    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        raise NotImplementedError()

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[dict]:
        raise NotImplementedError()

    async def save_conversation(self, conversation: dict) -> None:
        raise NotImplementedError()

    async def list_conversations(self, user_id: str) -> List[dict]:
        raise NotImplementedError()
