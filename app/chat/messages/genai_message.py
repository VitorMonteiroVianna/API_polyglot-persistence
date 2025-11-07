from dataclasses import dataclass

from app.chat.messages.message import Message
from app.chat.tokens import GenaiModelUsage


@dataclass
class GenaiMessage(Message):
    """
    Classe usada para armazenar uma mensagem que retornada pelo modelo
    de Gen AI. 
    """
    user_message_id: str
    genai_role: str
    genai_usage: GenaiModelUsage | None = None
    user_id: str | None = None

    def as_dict(self) -> dict:
        data = super().as_dict()
        data["user_message_id"] = self.user_message_id
        data["genai_role"] = self.genai_role
        if self.genai_usage:
            data["genai_usage"] = self.genai_usage.model_dump()
        if self.user_id is not None:
            data["user_id"] = self.user_id
        return data