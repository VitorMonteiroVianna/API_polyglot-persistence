from abc import ABC, abstractmethod
from typing import List, Optional

from app.chat.messages.user_message import UserMessage
from app.chat.messages.genai_message import GenaiMessage


class ChatRepository(ABC):
    @abstractmethod
    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        ...

    @abstractmethod
    async def append_user_message(self, message: UserMessage) -> None:
        ...

    @abstractmethod
    async def append_genai_message(self, message: GenaiMessage) -> None:
        ...

    @abstractmethod
    async def list_messages(self, user_id: str, conversation_id: str) -> List[dict]:
        ...

    @abstractmethod
    async def list_conversations(self, user_id: str) -> List[dict]:
        ...